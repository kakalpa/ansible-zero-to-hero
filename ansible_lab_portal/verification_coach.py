import os
import re
import yaml
import subprocess
import time

def analyze_yaml_text(content: str):
    """
    Performs pre-flight static analysis on student YAML content.
    Returns a list of warnings or fatal errors with actionable suggestions.
    """
    issues = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, 1):
        # Check for unquoted Jinja2 template at the start of a value: e.g. `path: {{ var }}`
        unquoted_jinja = re.search(r':\s+({{.+?}})', line)
        if unquoted_jinja:
            matched = unquoted_jinja.group(1)
            raw_val = line.split(":", 1)[1].strip()
            if not (raw_val.startswith('"') or raw_val.startswith("'")):
                issues.append({
                    "line": idx,
                    "type": "error",
                    "code": "UNQUOTED_JINJA_VAR",
                    "message": f"Line {idx}: Unquoted Jinja2 expression `{matched}`.",
                    "tip": "YAML syntax error: Any value starting with a curly brace `{{` must be enclosed in quotes. Use quotes: `path: \"{{ var }}\"`."
                })

        # Check for `when:` wrapped in `{{ }}`
        when_match = re.search(r'^\s*when:\s*([\'"].*?{{.*?}}.*?[\'"]|{{.*?}})', line)
        if when_match:
            issues.append({
                "line": idx,
                "type": "warning",
                "code": "JINJA_IN_WHEN_CLAUSE",
                "message": f"Line {idx}: Jinja2 delimiters `{{{{ }}}}` found inside `when:` clause.",
                "tip": "In Ansible, `when:` statements are already evaluated as Python/Jinja2 expressions. Remove the outer `{{ }}` (e.g. `when: ansible_facts['os_family'] == 'Debian'`)."
            })

        # Check for raw shell/command anti-patterns
        shell_mkdir = re.search(r'^\s*(?:ansible\.builtin\.)?(?:shell|command):\s*(?:mkdir|touch|rm\s+-rf)\b', line)
        if shell_mkdir:
            issues.append({
                "line": idx,
                "type": "warning",
                "code": "SHELL_INSTEAD_OF_FILE",
                "message": f"Line {idx}: Non-declarative shell/command detected for file/directory operation.",
                "tip": "Best practice: Use the declarative `ansible.builtin.file` module with `state: directory`, `state: touch`, or `state: absent` to guarantee idempotency."
            })

    return issues

def parse_play_recap(output: str):
    """
    Parses the PLAY RECAP from ansible-playbook output.
    Returns dict mapping host -> dict of stats (ok, changed, unreachable, failed)
    """
    recap = {}
    lines = output.splitlines()
    in_recap = False
    for line in lines:
        if "PLAY RECAP" in line:
            in_recap = True
            continue
        if in_recap and line.strip():
            m = re.match(r'^\s*([^\s:]+)\s*:\s*ok=(\d+)\s+changed=(\d+)\s+unreachable=(\d+)\s+failed=(\d+)', line)
            if m:
                host = m.group(1)
                recap[host] = {
                    "ok": int(m.group(2)),
                    "changed": int(m.group(3)),
                    "unreachable": int(m.group(4)),
                    "failed": int(m.group(5))
                }
    return recap

def run_idempotency_check(playbook_path: str, cwd: str, timeout: int = 60):
    """
    Executes a second run of the specified playbook and asserts changed == 0.
    Returns (is_idempotent: bool, changed_hosts: list, details: str)
    """
    if not os.path.exists(playbook_path):
        return True, [], "Playbook not found; skipping idempotency check."

    cmd = ["ansible-playbook", playbook_path]
    env = os.environ.copy()
    env["ANSIBLE_LOG_PATH"] = "/dev/null"

    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout
        )
        recap = parse_play_recap(proc.stdout)
        changed_hosts = [h for h, stats in recap.items() if stats.get("changed", 0) > 0]
        failed_hosts = [h for h, stats in recap.items() if stats.get("failed", 0) > 0 or stats.get("unreachable", 0) > 0]

        if failed_hosts:
            return False, failed_hosts, f"Playbook failed on second run for hosts: {', '.join(failed_hosts)}"
        if changed_hosts:
            return False, changed_hosts, f"Idempotency violation: The playbook reported changes on its second run for hosts: {', '.join(changed_hosts)}"
        return True, [], "Playbook is strictly idempotent (0 changes on second execution)."
    except subprocess.TimeoutExpired:
        return False, [], "Idempotency check timed out."
    except Exception as e:
        return False, [], f"Idempotency check error: {str(e)}"

def format_coaching_report(raw_output: str, ex: dict = None) -> str:
    """
    Inspects raw Ansible output for common student failure modes and generates
    a formatted SRE Coaching Box with root cause and actionable remedy.
    """
    coaching = []

    # 1. Unquoted Jinja2 Scanner Error
    if "ScannerError" in raw_output or "while scanning for the next token" in raw_output:
        if "{{" in raw_output:
            coaching.append(
                "💡 **SRE Coaching — YAML Syntax Rule**:\n"
                "   In YAML, any value starting with a curly brace `{{` must be enclosed in quotes.\n"
                "   Example: `path: \"{{ app_root }}\"` (not `path: {{ app_root }}`)."
            )

    # 2. Bare variable in when clause
    if "The conditional check" in raw_output and "{{" in raw_output:
        coaching.append(
            "💡 **SRE Coaching — Conditional Antipattern**:\n"
            "   Expressions inside `when:` clauses are already treated as Jinja2 expressions.\n"
            "   Do not wrap variables in `{{ }}` inside a `when:` block (e.g., use `when: ansible_facts['os_family'] == 'Debian'`)."
        )

    # 3. Missing file / Playbook file not found
    if "failed_when: not p_st.stat.exists" in raw_output or "stat.exists == false" in raw_output or '"exists": false' in raw_output or "No such file or directory" in raw_output:
        target_file = ex.get("target_file", "the requested playbook file") if ex else "the playbook"
        coaching.append(
            f"💡 **SRE Coaching — Missing Artifact**:\n"
            f"   Verification could not locate `{target_file}`.\n"
            f"   Ensure you created and saved the file with the exact name requested in the scenario briefing."
        )

    # 4. Command audit log empty or missing command
    if "failed_when: chk.rc != 0" in raw_output:
        coaching.append(
            "💡 **SRE Coaching — Command Execution Audit**:\n"
            "   The required command was not detected in the interactive terminal audit log.\n"
            "   Make sure you execute the command directly in the interactive shell terminal."
        )

    # 5. Missing become / Permission Denied
    if "Permission denied" in raw_output or "as root" in raw_output:
        coaching.append(
            "💡 **SRE Coaching — Privilege Escalation**:\n"
            "   Task encountered a permission denial. Does this action require root privileges or `become: true`?"
        )

    # 6. Syntax check failed
    if "ERROR! Syntax Error while loading YAML" in raw_output:
        coaching.append(
            "💡 **SRE Coaching — YAML Indentation**:\n"
            "   YAML is indentation-sensitive (use 2 spaces, never tabs). Ensure list items (`-`) and attributes line up properly."
        )

    if coaching:
        header = (
            "\n"
            "======================================================================\n"
            "🎓 SRE COACHING & ROOT CAUSE ANALYSIS (RCA)\n"
            "======================================================================\n"
        )
        return raw_output + header + "\n\n".join(coaching) + "\n"
    return raw_output

def clean_task_text(t: str) -> str:
    """Strips leading numbering like '1. ' or '1) ' from task strings."""
    return re.sub(r'^\d+[\.\)]\s*', '', t).strip()

def prepare_resilient_validation_playbook(playbook_text: str, project_dir: str = None) -> str:
    """
    Safely injects ignore_errors: true on every task in the validation playbook.
    Also ensures any task executing ansible-playbook via command/shell has
    the inventory specified and runs in the proper project directory.
    """
    inv_path = "/ansible/inventory.ini"
    work_dir = "/ansible"
    if project_dir and os.path.exists(project_dir):
        work_dir = project_dir
        cand_inv = os.path.join(project_dir, "inventory.ini")
        if os.path.exists(cand_inv):
            inv_path = cand_inv

    try:
        data = yaml.safe_load(playbook_text)
        if isinstance(data, list):
            for play in data:
                if isinstance(play, dict):
                    for task in play.get("tasks", []):
                        if isinstance(task, dict):
                            task["ignore_errors"] = True
                            # Check for ansible-playbook in command/shell
                            for mod in ["command", "ansible.builtin.command", "shell", "ansible.builtin.shell"]:
                                if mod in task and isinstance(task[mod], str) and "ansible-playbook" in task[mod]:
                                    cmd_str = task[mod]
                                    if "-i " not in cmd_str and "--inventory" not in cmd_str:
                                        task[mod] = cmd_str.replace("ansible-playbook", f"ansible-playbook -i {inv_path}")
                                    if "args" not in task:
                                        task["args"] = {}
                                    if "chdir" not in task["args"]:
                                        task["args"]["chdir"] = work_dir
            return yaml.dump(data, sort_keys=False)
    except Exception:
        pass
    return playbook_text

def parse_ansible_task_execution(raw_output: str) -> list:
    """
    Parses task-by-task execution results from ansible-playbook stdout.
    Returns a list of dicts with task name, pass/fail status, and diagnostic badges.
    """
    blocks = re.split(r'TASK \[(.*?)\] \*+', raw_output)
    executed_tasks = []
    for i in range(1, len(blocks), 2):
        task_name = blocks[i].strip()
        body = blocks[i+1] if i+1 < len(blocks) else ''
        
        is_failed = bool(re.search(r'(fatal|failed): \[.*?\]: FAILED!', body))
        has_ok_or_changed = bool(re.search(r'(ok|changed): \[.*?\]', body))
        
        error_badge = ''
        detail = ''
        if is_failed:
            m_assert = re.search(r'\"assertion\": \"(.*?)\"', body)
            m_msg = re.search(r'\"msg\": \"(.*?)\"', body)
            if m_assert:
                assertion_expr = m_assert.group(1)
                if ' in ' in assertion_expr:
                    error_badge = 'wrong content 👎'
                    detail = f"Assertion failed: {assertion_expr}"
                elif 'not ' in assertion_expr and 'exists' in assertion_expr:
                    error_badge = 'file still exists 👎'
                    detail = f"Target artifact was not deleted: {assertion_expr}"
                elif 'exists' in assertion_expr:
                    error_badge = 'file missing 👎'
                    detail = f"Expected file not found: {assertion_expr}"
                elif any(k in assertion_expr for k in ['proc', 'pkill', 'sleep', 'ps']):
                    error_badge = 'process still running 👎'
                    detail = f"Rogue process active: {assertion_expr}"
                elif 'mode' in assertion_expr:
                    error_badge = 'incorrect permissions 👎'
                    detail = f"File permissions mismatch: {assertion_expr}"
                else:
                    error_badge = 'assertion failed 👎'
                    detail = assertion_expr
            elif "skipping: no hosts matched" in body:
                error_badge = 'no hosts matched 👎'
                detail = 'Inventory hosts did not match target group'
            elif "Device or resource busy" in body or "Errno 16" in body:
                error_badge = 'bind-mount error 👎 (add unsafe_writes: true)'
                detail = 'Target file is a Docker bind-mount. Add "unsafe_writes: true" to lineinfile/copy to allow in-place edits.'
            elif m_msg:
                msg_val = m_msg.group(1).strip()
                if not msg_val or msg_val == "''" or msg_val == '""':
                    if "not in" in body:
                        error_badge = 'wrong content 👎'
                        detail = 'Expected text not found in command output'
                    else:
                        error_badge = 'execution failed 👎'
                        detail = 'Command execution failed'
                elif 'Assertion failed' in msg_val:
                    error_badge = 'wrong content 👎'
                    detail = msg_val
                else:
                    error_badge = f'failed 👎 ({msg_val})'
                    detail = msg_val
            elif 'No such file or directory' in body:
                error_badge = 'file missing 👎'
                detail = 'File or directory not found'
            else:
                error_badge = 'execution failed 👎'
                detail = 'Task condition not satisfied'

        executed_tasks.append({
            'name': task_name,
            'failed': is_failed,
            'passed': has_ok_or_changed and not is_failed,
            'error_badge': error_badge,
            'detail': detail,
            'body': body
        })
    return executed_tasks

def match_exercise_tasks(exercise: dict, executed_tasks: list, overall_passed: bool, target_file_path: str = None) -> list:
    """
    Correlates executed Ansible validation tasks with the exercise's checklist items.
    Returns structured results for each checklist task:
    [{ 'index': 1, 'text': '...', 'status': 'passed'|'failed'|'pending', 'badge': 'done 👍'|'wrong content 👎', 'detail': '...' }]
    """
    raw_tasks = exercise.get('tasks', [])
    if not raw_tasks:
        return []

    results = []
    if overall_passed:
        for idx, t in enumerate(raw_tasks, 1):
            results.append({
                'index': idx,
                'text': clean_task_text(t),
                'status': 'passed',
                'badge': 'done 👍',
                'detail': ''
            })
        return results

    # If the exercise requires an authored playbook file on disk
    target_content = None
    if target_file_path and os.path.exists(target_file_path):
        try:
            with open(target_file_path, "r") as f:
                target_content = f.read()
        except Exception:
            pass

    assert_tasks = [t for t in executed_tasks if t['name'].lower().startswith(('assert', 'verify')) or t['failed']]
    if not assert_tasks:
        assert_tasks = executed_tasks

    # If we have target_content and it's a playbook authoring exercise
    if target_content:
        for idx, t in enumerate(raw_tasks, 1):
            t_clean = clean_task_text(t)
            t_lower = t_clean.lower()
            
            # 1. Execution task
            if any(k in t_lower for k in ['run ansible-playbook', 'execute ansible-playbook', 'run the playbook']):
                has_exec_fail = any(at['failed'] for at in executed_tasks)
                if has_exec_fail:
                    fail_t = next((at for at in executed_tasks if at['failed']), None)
                    badge = fail_t['error_badge'] if fail_t else 'execution failed 👎'
                    detail = fail_t['detail'] if fail_t else 'Playbook execution failed'
                    results.append({
                        'index': idx,
                        'text': t_clean,
                        'status': 'failed',
                        'badge': badge,
                        'detail': detail
                    })
                else:
                    results.append({
                        'index': idx,
                        'text': t_clean,
                        'status': 'passed',
                        'badge': 'done 👍',
                        'detail': ''
                    })
                continue

            # 2. Authoring check: Author/target hosts
            if ('author' in t_lower or 'create' in t_lower) and 'targeting' in t_lower:
                target_group = exercise.get('target', 'all')
                if f'hosts: {target_group}' in target_content or f'hosts:\n  - {target_group}' in target_content or 'hosts:' in target_content:
                    results.append({
                        'index': idx,
                        'text': t_clean,
                        'status': 'passed',
                        'badge': 'done 👍',
                        'detail': ''
                    })
                    continue

            # 3. Module / directive check
            known_modules = ['debug', 'copy', 'file', 'template', 'service', 'lineinfile', 'blockinfile', 'user', 'apt', 'dnf', 'package', 'command', 'shell', 'stat', 'assert']
            found_mod = next((m for m in known_modules if m in t_lower), None)
            if found_mod and (found_mod in target_content or f'ansible.builtin.{found_mod}' in target_content):
                m_param = re.search(r'parameter\s+([a-zA-Z0-9_]+)', t_lower)
                if m_param:
                    param_name = m_param.group(1)
                    if f'{param_name}:' in target_content:
                        results.append({
                            'index': idx,
                            'text': t_clean,
                            'status': 'passed',
                            'badge': 'done 👍',
                            'detail': ''
                        })
                        continue
                else:
                    results.append({
                        'index': idx,
                        'text': t_clean,
                        'status': 'passed',
                        'badge': 'done 👍',
                        'detail': ''
                    })
                    continue

            # 4. Quoted string value check (e.g. Set msg to 'DataForge Automation Active')
            quoted_strings = re.findall(r"['\"]([^'\"]+)['\"]", t)
            if quoted_strings and all(q in target_content for q in quoted_strings):
                results.append({
                    'index': idx,
                    'text': t_clean,
                    'status': 'passed',
                    'badge': 'done 👍',
                    'detail': ''
                })
                continue

            # 5. Fallback for remaining tasks
            matched_at = None
            for at in assert_tasks:
                at_name = at['name'].lower()
                words = [w for w in re.split(r'[^a-zA-Z0-9_\-\.]', at_name) if len(w) > 3 and w not in ('check', 'assert', 'verify', 'test')]
                if any(w in t_lower for w in words):
                    matched_at = at
                    break

            if matched_at and matched_at['failed']:
                results.append({
                    'index': idx,
                    'text': t_clean,
                    'status': 'failed',
                    'badge': matched_at['error_badge'] or 'failed 👎',
                    'detail': matched_at['detail'] or matched_at['name']
                })
            else:
                has_failed = any(at['failed'] for at in assert_tasks)
                results.append({
                    'index': idx,
                    'text': t_clean,
                    'status': 'passed' if not has_failed else 'pending',
                    'badge': 'done 👍' if not has_failed else 'pending ⏳',
                    'detail': ''
                })
        return results

    # If count of assertion tasks matches count of checklist items
    if len(assert_tasks) == len(raw_tasks):
        for idx, (t, at) in enumerate(zip(raw_tasks, assert_tasks), 1):
            if at['failed']:
                results.append({
                    'index': idx,
                    'text': clean_task_text(t),
                    'status': 'failed',
                    'badge': at['error_badge'] or 'failed 👎',
                    'detail': at['detail'] or at['name']
                })
            elif at['passed']:
                results.append({
                    'index': idx,
                    'text': clean_task_text(t),
                    'status': 'passed',
                    'badge': 'done 👍',
                    'detail': ''
                })
            else:
                results.append({
                    'index': idx,
                    'text': clean_task_text(t),
                    'status': 'pending',
                    'badge': 'not reached ⏳',
                    'detail': ''
                })
        return results

    # Semantic keyword correlation
    for idx, t in enumerate(raw_tasks, 1):
        t_clean = clean_task_text(t)
        t_lower = t_clean.lower()
        matched_at = None
        for at in assert_tasks:
            at_name = at['name'].lower()
            words = [w for w in re.split(r'[^a-zA-Z0-9_\-\.]', at_name) if len(w) > 3 and w not in ('check', 'assert', 'verify', 'test')]
            if any(w in t_lower for w in words):
                matched_at = at
                break

        if matched_at:
            if matched_at['failed']:
                results.append({
                    'index': idx,
                    'text': t_clean,
                    'status': 'failed',
                    'badge': matched_at['error_badge'] or 'failed 👎',
                    'detail': matched_at['detail'] or matched_at['name']
                })
            elif matched_at['passed']:
                results.append({
                    'index': idx,
                    'text': t_clean,
                    'status': 'passed',
                    'badge': 'done 👍',
                    'detail': ''
                })
            else:
                results.append({
                    'index': idx,
                    'text': t_clean,
                    'status': 'pending',
                    'badge': 'not reached ⏳',
                    'detail': ''
                })
        else:
            has_failed_assert = any(at['failed'] for at in assert_tasks)
            status = 'passed' if not has_failed_assert else 'pending'
            badge = 'done 👍' if not has_failed_assert else 'pending ⏳'
            results.append({
                'index': idx,
                'text': t_clean,
                'status': status,
                'badge': badge,
                'detail': ''
            })

    return results

def format_task_verification_report(exercise: dict, task_results: list, raw_output: str, preflight_error: dict = None, idempotency_error: str = None) -> str:
    """
    Formats an end-user friendly, human-readable validation summary.
    Lists each scenario task with clean emojis (done 👍 / wrong content 👎),
    followed by SRE coaching and collapsible technical logs.
    """
    lines = []
    lines.append("📋 Scenario Task Verification:\n")
    for r in task_results:
        idx = r.get("index", 1)
        text = r.get("text", "")
        badge = r.get("badge", "done 👍")
        lines.append(f"    {idx}. {text}  -- {badge}\n")

    lines.append("─" * 78)

    if preflight_error:
        lines.append(f"\n❌ Pre-Flight Static Analysis Failed ({preflight_error.get('code', 'Syntax Issue')}):")
        lines.append(f"   {preflight_error.get('message', '')}")
        lines.append(f"   💡 {preflight_error.get('tip', '')}\n")
        lines.append("─" * 78)

    if idempotency_error:
        lines.append(f"\n❌ Phase 3 Idempotency Check Failed:\n   {idempotency_error}\n")
        lines.append("─" * 78)

    has_failures = any(r.get("status") == "failed" for r in task_results) or preflight_error or idempotency_error
    if has_failures:
        coaching_box = format_coaching_report(raw_output, exercise)
        if "🎓 SRE COACHING & ROOT CAUSE ANALYSIS (RCA)" in coaching_box:
            parts = coaching_box.split("🎓 SRE COACHING & ROOT CAUSE ANALYSIS (RCA)")
            if len(parts) > 1:
                lines.append("\n🎓 SRE COACHING & ROOT CAUSE ANALYSIS (RCA)" + parts[1].rstrip())
                lines.append("─" * 78)

    lines.append("\n▼ Technical Ansible Playbook Execution Log:")
    lines.append(raw_output.strip() if raw_output else "(No output)")

    return "\n".join(lines)

