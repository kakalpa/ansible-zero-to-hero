import os
import sys
import tempfile
import subprocess
import time
import json
import pty
import fcntl
import termios
import struct
import io
import zipfile
import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional

PORTAL_DIR = os.path.dirname(os.path.abspath(__file__))
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)

from curriculum import MODULES, EXERCISES
import cluster_manager
import verification_coach
from terminal_manager import session_manager

PROJECT_DIR = os.getenv("PROJECT_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
session_manager.cwd = PROJECT_DIR

app = FastAPI(title="Ansible Zero-to-Hero Interactive Lab")

app.mount("/static", StaticFiles(directory=os.path.join(PORTAL_DIR, "static")), name="static")

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "version": "2.5.0",
        "service": "ansible-lab-portal",
        "nodes_configured": len(cluster_manager.NODES),
        "total_lessons": len(EXERCISES),
        "timestamp": time.time()
    }

class ExecuteRequest(BaseModel):
    code: str

class FileSaveRequest(BaseModel):
    path: str
    content: str

class FileCreateRequest(BaseModel):
    path: str
    content: Optional[str] = ""

def _resolve_safe_path(rel_path: str) -> str:
    """Ensure relative path stays strictly inside PROJECT_DIR."""
    rel = rel_path.strip().lstrip("/")
    if rel.startswith("ansible/"):
        rel = rel[len("ansible/"):]
    full_path = os.path.abspath(os.path.join(PROJECT_DIR, rel))
    if not full_path.startswith(os.path.abspath(PROJECT_DIR)):
        raise HTTPException(status_code=403, detail="Access denied: path traversal not permitted")
    return full_path

def _find_target_file_path(target_file: Optional[str]) -> Optional[str]:
    """Finds the actual existing path on disk for target_file across local and container layouts."""
    if not target_file:
        return None
    raw = target_file.strip()
    clean = raw
    if clean.startswith("/ansible/"):
        clean = clean[len("/ansible/"):]
    elif clean.startswith("ansible/"):
        clean = clean[len("ansible/"):]

    candidates = [
        os.path.join(PROJECT_DIR, clean),
        os.path.join(PROJECT_DIR, raw.lstrip("/")),
        os.path.join(PROJECT_DIR, "workspace", clean),
        os.path.join(PROJECT_DIR, "playbooks", clean),
        raw,
        os.path.join("/ansible", clean),
        os.path.join("/ansible/playbooks", clean)
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None

def _delete_target_file(target_file: Optional[str]):
    """Purges all occurrences of target_file on disk across all potential locations."""
    if not target_file:
        return
    raw = target_file.strip()
    clean = raw
    if clean.startswith("/ansible/"):
        clean = clean[len("/ansible/"):]
    elif clean.startswith("ansible/"):
        clean = clean[len("ansible/"):]

    candidates = {
        os.path.join(PROJECT_DIR, clean),
        os.path.join(PROJECT_DIR, raw.lstrip("/")),
        os.path.join(PROJECT_DIR, "workspace", clean),
        os.path.join(PROJECT_DIR, "playbooks", clean),
        raw,
        os.path.join("/ansible", clean),
        os.path.join("/ansible/playbooks", clean),
        "/tmp/solution.yml",
        "/ansible/solution.yml"
    }
    for p in candidates:
        try:
            if os.path.isfile(p):
                os.remove(p)
        except Exception:
            pass

def run_ansible_playbook(playbook_content: str):
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
        f.write(playbook_content)
        temp_path = f.name

    try:
        start_time = time.time()
        cmd = ["ansible-playbook", temp_path]
        env = os.environ.copy()
        env["ANSIBLE_LOG_PATH"] = "/dev/null"
        env["ANSIBLE_CONFIG"] = os.path.join(PROJECT_DIR, "ansible.cfg")
        env["ANSIBLE_INVENTORY"] = os.path.join(PROJECT_DIR, "inventory.ini")
        proc = subprocess.run(
            cmd,
            cwd=PROJECT_DIR,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=90
        )
        duration = round(time.time() - start_time, 2)
        return {
            "success": proc.returncode == 0,
            "output": proc.stdout,
            "returncode": proc.returncode,
            "duration": duration
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "Execution timed out after 90 seconds.",
            "returncode": -1,
            "duration": 90.0
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def run_ansible_command(command_str: str):
    try:
        start_time = time.time()
        env = os.environ.copy()
        env["ANSIBLE_CONFIG"] = os.path.join(PROJECT_DIR, "ansible.cfg")
        env["ANSIBLE_INVENTORY"] = os.path.join(PROJECT_DIR, "inventory.ini")
        proc = subprocess.run(
            command_str,
            shell=True,
            cwd=PROJECT_DIR,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60
        )
        duration = round(time.time() - start_time, 2)
        return {
            "success": proc.returncode == 0,
            "output": proc.stdout,
            "returncode": proc.returncode,
            "duration": duration
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "Command timed out after 60 seconds.",
            "returncode": -1,
            "duration": 60.0
        }

@app.get("/", response_class=HTMLResponse)
def index():
    with open(os.path.join(PORTAL_DIR, "templates", "index.html"), "r") as f:
        return f.read()

@app.get("/api/curriculum")
def get_curriculum():
    return {
        "modules": MODULES,
        "exercises": EXERCISES
    }

@app.get("/api/cluster/status")
def cluster_status():
    nodes = cluster_manager.get_cluster_status()
    return {"nodes": nodes}

@app.get("/api/cluster/telemetry/stream")
async def cluster_telemetry_stream():
    """Server-Sent Events endpoint streaming live 6-node cluster metrics every 2s."""
    async def event_generator():
        while True:
            try:
                telemetry = await cluster_manager.get_async_cluster_telemetry()
                data_str = json.dumps(telemetry)
                yield f"data: {data_str}\n\n"
            except Exception:
                yield "data: []\n\n"
            await asyncio.sleep(2.0)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/cluster/rollback")
def cluster_rollback():
    success, log = cluster_manager.rollback_entire_cluster()
    if not success:
        raise HTTPException(status_code=500, detail=log)
    return {"success": True, "log": log}

# ==========================================================
# WORKSPACE FILE API (IN-BROWSER EDITOR INTEGRATION)
# ==========================================================
@app.get("/api/files")
def list_workspace_files():
    """Returns editable files in the project workspace."""
    results = []
    allowed_exts = {".yml", ".yaml", ".ini", ".cfg", ".j2", ".sh", ".json", ".txt"}
    ignored_names = {".lab_bash_history", "__pycache__", ".git", ".ansible_audit_log"}

    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "ansible_lab_portal")]
        for f in files:
            if f in ignored_names or f.startswith("."):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in allowed_exts or f in ("ansible.cfg", "inventory", "hosts"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, PROJECT_DIR)
                size = os.path.getsize(full_path)
                mtime = os.path.getmtime(full_path)
                results.append({
                    "name": f,
                    "path": rel_path,
                    "size": size,
                    "mtime": mtime,
                    "ext": ext.lstrip(".") or "txt"
                })

    results.sort(key=lambda x: (x["ext"] not in ("yml", "yaml"), x["path"]))
    return {"files": results}

@app.get("/api/files/content")
def get_file_content(path: str):
    """Reads content of a workspace file."""
    safe_path = _resolve_safe_path(path)
    if not os.path.isfile(safe_path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with open(safe_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return {"path": path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/save")
def save_file_content(req: FileSaveRequest):
    """Saves content to a workspace file."""
    safe_path = _resolve_safe_path(req.path)
    parent_dir = os.path.dirname(safe_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    try:
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(req.content)
        return {"success": True, "path": req.path, "bytes": len(req.content)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/create")
def create_workspace_file(req: FileCreateRequest):
    """Creates a new workspace file."""
    safe_path = _resolve_safe_path(req.path)
    parent_dir = os.path.dirname(safe_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    try:
        if not os.path.exists(safe_path):
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(req.content or "")
        return {"success": True, "path": req.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workspace/export")
def export_workspace_repo():
    """Bundles authored playbooks, configs, and generates a personalized portfolio README.md into a ZIP archive."""
    allowed_exts = {".yml", ".yaml", ".ini", ".cfg", ".j2", ".sh", ".json", ".txt", ".md"}
    ignored_names = {".lab_bash_history", "__pycache__", ".git", ".ansible_audit_log", ".DS_Store"}

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # Collect all project files
        for root, dirs, files in os.walk(PROJECT_DIR):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "ansible_lab_portal")]
            for f in files:
                if f in ignored_names or f.startswith("."):
                    continue
                ext = os.path.splitext(f)[1].lower()
                if ext in allowed_exts or f in ("ansible.cfg", "inventory", "hosts"):
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, PROJECT_DIR)
                    try:
                        zf.write(full_path, arcname=f"ansible-lab-portfolio/{rel_path}")
                    except Exception:
                        pass

        # Synthesize a polished README.md for the portfolio
        readme_content = """# 🚀 DataForge SRE Fleet Automation Portfolio

Production-grade Ansible automation playbooks, multi-distro fleet management configurations, and SRE incident response remediations developed and verified against a live 6-node heterogeneous Linux cluster.

## 🏗️ Multi-Distro Fleet Architecture
- **Control Plane**: Dedicated Ansible Control Node (Python 3, Ansible Core)
- **Target Nodes**:
  - `node1-ubuntu` (Ubuntu 22.04 LTS / Jammy)
  - `node2-debian` (Debian 12 Bookworm)
  - `node3-debian13` (Debian 13 Trixie Next-Gen)
  - `node4-almalinux` (AlmaLinux 9 Enterprise)
  - `node5-rocky` (Rocky Linux 9 Enterprise)
  - `node6-alpine` (Alpine Linux 3.22 Musl/BusyBox)

## 📁 Repository Structure
```
ansible-lab-portfolio/
├── ansible.cfg              # Tuned control plane configuration (pipelining, forks, host_key_checking)
├── inventory.ini            # Heterogeneous inventory groups (webservers, dbservers, appservers, multi_os)
├── *.yml                    # Modular playbooks across Levels 1-4 (Setup, Security, SRE Ops, Chaos)
└── roles/                   # Reusable Ansible Galaxy-style automation roles
```

## 🛡️ SRE Highlights & Competencies Demonstrated
1. **Ad-Hoc Fleet Orchestration**: High-throughput multi-node diagnostics, package queries, and service management.
2. **Declarative State & Convergence**: Package managers across Debian (`apt`), RHEL (`dnf`), and Alpine (`apk`).
3. **Idempotent Automation**: All playbooks verified with strict 0-change 2nd-pass idempotency assertions.
4. **Chaos Engineering & Root Cause Analysis (RCA)**: Remediated complex multi-tier incidents under simulated MTTR conditions.

---
*Authored with the Ansible Zero-to-Hero Interactive Lab Platform.*
"""
        zf.writestr("ansible-lab-portfolio/README.md", readme_content)

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=ansible-lab-portfolio.zip"
        }
    )

@app.post("/api/exercise/{ex_id}/execute")
def execute_exercise(ex_id: str, req: ExecuteRequest):
    ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    code = req.code.strip()
    if not code:
        code = ex["solution_code"]

    target = ex.get("target", "all")
    cluster_manager.mark_node_activity(target, is_changed=True)

    if code.startswith("ansible "):
        result = run_ansible_command(code)
    else:
        result = run_ansible_playbook(code)
    return result

@app.post("/api/exercise/{ex_id}/setup")
def setup_exercise(ex_id: str):
    ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    setup_playbook = ex.get("setup_playbook") or ex.get("reset_playbook")
    if setup_playbook:
        result = run_ansible_playbook(setup_playbook)
    else:
        result = {"success": True, "output": "Environment ready."}

    # Clear user execution log when entering scenario so prior commands do not carry over
    try:
        with open("/var/log/ansible.log", "w") as f:
            f.write("")
    except Exception:
        pass

    return result

@app.post("/api/exercise/{ex_id}/reset")
def reset_exercise(ex_id: str):
    ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    target_file = ex.get("target_file")
    if target_file:
        _delete_target_file(target_file)

    for tmp_f in ["/tmp/solution.yml", "/ansible/solution.yml"]:
        if os.path.exists(tmp_f):
            try:
                os.remove(tmp_f)
            except Exception:
                pass

    reset_playbook = ex.get("reset_playbook") or ex.get("setup_playbook")
    if reset_playbook:
        result = run_ansible_playbook(reset_playbook)
    else:
        result = {"success": True, "output": "No cleanup required for this exercise."}

    # Clear user execution log after reset so doing nothing cannot pass
    try:
        with open("/var/log/ansible.log", "w") as f:
            f.write("")
    except Exception:
        pass

    result["target_file_reset"] = True
    return result

@app.post("/api/exercise/{ex_id}/validate")
def validate_exercise(ex_id: str):
    ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    target_file = ex.get("target_file")
    real_target_file = _find_target_file_path(target_file) if target_file else None

    # If exercise requires a playbook file, it MUST exist to validate
    if target_file and not real_target_file:
        clean_name = target_file.replace("/ansible/", "")
        task_results = [
            {
                "index": 1,
                "text": f"Author target playbook '{clean_name}'",
                "status": "failed",
                "badge": "file missing 👎",
                "detail": f"File '{clean_name}' does not exist on disk"
            }
        ]
        for idx, t in enumerate(ex.get("tasks", [])[1:], 2):
            task_results.append({
                "index": idx,
                "text": verification_coach.clean_task_text(t),
                "status": "pending",
                "badge": "pending ⏳",
                "detail": ""
            })
        msg = f"Playbook file '{clean_name}' does not exist on disk.\nPlease author and save your playbook in the editor or terminal before verifying."
        output_report = verification_coach.format_task_verification_report(ex, task_results, msg)
        return {
            "success": True,
            "passed": False,
            "output": output_report,
            "tasks_results": task_results,
            "duration": 0.01
        }

    # Phase 1: Pre-Flight Static Analysis (Fast Fail on YAML Antipatterns)
    if real_target_file:
        try:
            with open(real_target_file, "r") as f:
                content = f.read()
            preflight_issues = verification_coach.analyze_yaml_text(content)
            fatal_errors = [i for i in preflight_issues if i["type"] == "error"]
            if fatal_errors:
                task_results = [
                    {
                        "index": 1,
                        "text": f"YAML syntax validation for {os.path.basename(real_target_file)}",
                        "status": "failed",
                        "badge": f"syntax error 👎 (Line {fatal_errors[0]['line']})",
                        "detail": fatal_errors[0]["message"]
                    }
                ]
                for idx, t in enumerate(ex.get("tasks", [])[1:], 2):
                    task_results.append({
                        "index": idx,
                        "text": verification_coach.clean_task_text(t),
                        "status": "pending",
                        "badge": "pending ⏳",
                        "detail": ""
                    })
                output_report = verification_coach.format_task_verification_report(
                    ex, task_results, fatal_errors[0]["message"], preflight_error=fatal_errors[0]
                )
                return {
                    "success": True,
                    "passed": False,
                    "output": output_report,
                    "tasks_results": task_results,
                    "duration": 0.05
                }
        except Exception:
            pass

    validation_playbook = ex.get("validation_playbook")
    if not validation_playbook:
        task_results = verification_coach.match_exercise_tasks(ex, [], True)
        output_report = verification_coach.format_task_verification_report(ex, task_results, "Self-validated exercise.")
        return {
            "success": True,
            "passed": True,
            "output": output_report,
            "tasks_results": task_results,
            "duration": 0.01
        }

    # Phase 2: Execution & Convergence Check (Resilient: execute all tasks)
    resilient_playbook = verification_coach.prepare_resilient_validation_playbook(validation_playbook, PROJECT_DIR)
    result = run_ansible_playbook(resilient_playbook)

    executed_tasks = verification_coach.parse_ansible_task_execution(result["output"])
    has_failed_task = any(t["failed"] for t in executed_tasks)
    recap = verification_coach.parse_play_recap(result["output"])
    has_failed_hosts = any(h.get("failed", 0) > 0 or h.get("ignored", 0) > 0 for h in recap.values())

    passed = (result["returncode"] == 0 or not has_failed_task) and not has_failed_task and not has_failed_hosts

    # Phase 3: Automated Idempotency Verification (For declarative playbooks)
    idemp_error = None
    if passed and real_target_file and ex.get("requires_idempotency", True):
        is_idemp, changed_hosts, idemp_details = verification_coach.run_idempotency_check(real_target_file, PROJECT_DIR)
        if not is_idemp:
            passed = False
            idemp_error = f"Idempotency violation: Changes reported on {', '.join(changed_hosts)}\n{idemp_details}"
        if changed_hosts:
            for h in changed_hosts:
                cluster_manager.mark_node_activity(h, is_changed=True)

    if passed:
        target = ex.get("target", "all")
        cluster_manager.mark_node_activity(target, is_changed=True)

    task_results = verification_coach.match_exercise_tasks(ex, executed_tasks, passed, real_target_file)
    formatted_report = verification_coach.format_task_verification_report(
        ex, task_results, result["output"], idempotency_error=idemp_error
    )

    return {
        "success": True,
        "passed": passed,
        "output": formatted_report,
        "tasks_results": task_results,
        "duration": result["duration"]
    }

# Interactive In-Browser Persistent PTY Terminal WebSocket
@app.websocket("/ws/terminal")
async def terminal_websocket(websocket: WebSocket):
    await websocket.accept()
    await session_manager.register_client(websocket)

    try:
        while True:
            msg = await websocket.receive_text()
            try:
                payload = json.loads(msg)
                mtype = payload.get("type")
                if mtype == "input":
                    session_manager.write_input(payload["data"].encode())
                elif mtype == "resize":
                    cols = payload.get("cols", 80)
                    rows = payload.get("rows", 24)
                    session_manager.resize_pty(cols, rows)
                elif mtype == "reset":
                    session_manager.reset_session()
            except json.JSONDecodeError:
                # Raw text fallback
                session_manager.write_input(msg.encode())
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        session_manager.unregister_client(websocket)

import inspect_helper

@app.post("/api/exercise/{ex_id}/inspect")
def inspect_exercise_node_state(ex_id: str):
    ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    cmd = ex.get("inspect_cmd", "uname -a")
    target = ex.get("target", "all")
    output = inspect_helper.inspect_node_state(cmd, target)
    return {
        "command": cmd,
        "target": target,
        "output": output
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
