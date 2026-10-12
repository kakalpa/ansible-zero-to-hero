# Level 1: Fleet Discovery & Ad-Hoc Recon (Lessons 1.1 to 1.11)

LEVEL1_EXERCISES = [   {   'difficulty': 'Beginner',
        'explanation': '### How It Works\n'
                       '\n'
                       "Ansible's `ping` module is **not** an ICMP network ping (packet bounce). Instead:\n"
                       '1. It connects to each remote host over SSH using your credentials (`root` with '
                       '`~/.ssh/master`).\n'
                       '2. It tests whether Python 3 is installed and executable on the target.\n'
                       '3. It returns JSON `{"ping": "pong"}` to confirm the host is fully ready for Ansible '
                       'management.\n'
                       '\n'
                       '#### Command:\n'
                       '```bash\n'
                       'ansible all -m ping\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Ad-hoc CLI Structure',
                         'text': 'Ansible ad-hoc commands follow the format: `ansible <pattern> -m <module>`.'},
                     {'level': 'Hint 2: The Command', 'text': 'Run `ansible all -m ping` in the terminal.'}],
        'id': 'l1-1-first-contact',
        'inspect_cmd': 'uname -n',
        'module': 'lvl1',
        'primer': {   'concept': "Ansible's `ping` module is **not** an ICMP network ping (packet bounce). It connects "
                                 'to each remote host over SSH, verifies Python interpreter availability, and returns '
                                 'JSON `{"ping": "pong"}` confirming the node is ready for management.',
                      'demo_code': 'ansible <target_group> -m ping',
                      'quick_tip': "To target every host defined in your inventory at once, use the built-in 'all' "
                                   'keyword.',
                      'syntax_breakdown': [   {'element': 'ansible', 'role': 'The Ansible ad-hoc CLI executable'},
                                              {   'element': 'all',
                                                  'role': 'Host pattern targeting every host in inventory'},
                                              {   'element': '-m ping',
                                                  'role': 'Specifies the module to invoke on remote targets'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.1\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: No state changes needed\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'Welcome to **DataForge Systems**! You have joined as an Infrastructure & Automation Engineer.\n'
                    '\n'
                    'Your first assignment from the Infrastructure Lead:\n'
                    '> *"We maintain a 6-node heterogeneous cluster running Ubuntu, Debian, AlmaLinux, Rocky Linux, '
                    'and Alpine. Before touching any configurations, we need to verify SSH connectivity and Python '
                    'runtime readiness across the entire cluster without altering any system state."*\n'
                    '\n'
                    "Use Ansible's ad-hoc runner to execute a baseline connectivity ping against all nodes.",
        'solution_code': 'ansible all -m ping',
        'solution_type': 'command',
        'target': 'all',
        'tasks': [   '1. Connect to all 6 nodes simultaneously using the ad-hoc runner.',
                     '2. Test baseline SSH and Python interpreter responsiveness across the fleet.',
                     '3. Verify that every node in the cluster acknowledges health with an affirmative response.'],
        'title': 'Lesson 1.1: First Contact — Pinging the Fleet',
        'validation_playbook': '---\n'
                               '- name: Validate 1.1\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify ping execution for all nodes in audit log\n'
                               '      ansible.builtin.shell: |\n'
                               "        grep -q 'node1-ubuntu | SUCCESS' /var/log/ansible.log && \\\n"
                               "        grep -q 'node6-alpine | SUCCESS' /var/log/ansible.log && \\\n"
                               '        grep -q \'"ping": "pong"\' /var/log/ansible.log\n'
                               '      register: chk\n'
                               '      failed_when: chk.rc != 0\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### Targeting Specific Host Groups\n'
                       '\n'
                       'In `inventory.ini`, hosts are categorized into groups under `[group_name]` headers:\n'
                       '```ini\n'
                       '[debian]\n'
                       'node2-debian\n'
                       'node3-debian13\n'
                       '```\n'
                       '\n'
                       'When you specify `ansible debian -m ping`, Ansible searches inventory for the `[debian]` group '
                       'and limits execution exclusively to those hosts.\n'
                       '\n'
                       '#### Command:\n'
                       '```bash\n'
                       'ansible debian -m ping\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Targeting Groups',
                         'text': 'Replace the `all` keyword from Lesson 1.1 with the group name: `debian`.'},
                     {'level': 'Hint 2: Command Syntax', 'text': 'Run `ansible debian -m ping`.'}],
        'id': 'l1-2-group-targeting',
        'inspect_cmd': "grep -A 3 '\\[debian\\]' /ansible/inventory.ini",
        'module': 'lvl1',
        'primer': {   'concept': 'Inventory files group servers into logical clusters (`[web]`, `[db]`, `[debian]`). '
                                 'Ad-hoc commands can target any specific group name directly instead of the global '
                                 '`all` pattern.',
                      'demo_code': 'ansible <group_name> -m <module_name>',
                      'quick_tip': 'Find group headers (like [web], [db], or [debian]) inside inventory.ini, then pass '
                                   'that exact group name.',
                      'syntax_breakdown': [   {'element': 'ansible', 'role': 'Ad-hoc command runner'},
                                              {   'element': 'debian',
                                                  'role': 'Inventory group name targeting node2-debian and '
                                                          'node3-debian13'},
                                              {   'element': '-m ping',
                                                  'role': 'Module to execute against the target group'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.2\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'In Lesson 1.1, you pinged every node with `all`. But in real production environments, you '
                    'frequently need to target only a subset of machines.\n'
                    '\n'
                    "DataForge's `inventory.ini` defines several logical groups:\n"
                    '- `ubuntu` (node1-ubuntu)\n'
                    '- `debian` (node2-debian, node3-debian13)\n'
                    '- `rhel` (node4-almalinux, node5-rocky)\n'
                    '- `alpine` (node6-alpine)\n'
                    '\n'
                    'Your team lead asks:\n'
                    '> *"We have an upcoming APT package upgrade scheduled. Ping ONLY the Debian group to ensure both '
                    'Debian nodes are responsive."*',
        'solution_code': 'ansible debian -m ping',
        'solution_type': 'command',
        'target': 'debian',
        'tasks': [   '1. Identify the logical group for Debian hosts in inventory.',
                     '2. Test connectivity targeting exclusively the Debian server slice.',
                     '3. Confirm that non-Debian nodes are excluded from the test run.'],
        'title': 'Lesson 1.2: Group Targeting — Exploring Inventory Slices',
        'validation_playbook': '---\n'
                               '- name: Validate 1.2\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify debian targeting in audit log\n'
                               '      ansible.builtin.shell: |\n'
                               "        grep -q 'node2-debian | SUCCESS' /var/log/ansible.log && \\\n"
                               "        grep -q 'node3-debian13 | SUCCESS' /var/log/ansible.log && \\\n"
                               '        grep -q \'"ping": "pong"\' /var/log/ansible.log\n'
                               '      register: chk\n'
                               '      failed_when: chk.rc != 0\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### Built-in Documentation with `ansible-doc`\n'
                       '\n'
                       '`ansible-doc` allows looking up parameter specifications without opening a web browser:\n'
                       '- `ansible-doc <module>`: Comprehensive man-page style documentation.\n'
                       '- `ansible-doc -s <module>`: Compact playbook YAML snippet showing all accepted parameters and '
                       'types.\n'
                       '- `ansible-doc -l`: List all available modules installed on your control system.\n'
                       '\n'
                       '#### Command:\n'
                       '```bash\n'
                       'ansible-doc -s ping\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Using ansible-doc',
                         'text': 'The `-s` flag produces a clean YAML snippet: `ansible-doc -s <module>`.'},
                     {'level': 'Hint 2: Exact Command', 'text': 'Run `ansible-doc -s ping` in the terminal.'}],
        'id': 'l1-3-ansible-doc',
        'inspect_cmd': 'ansible-doc --version',
        'module': 'lvl1',
        'primer': {   'concept': "`ansible-doc` is Ansible's built-in manual and documentation viewer. It describes "
                                 'module parameters, requirements, return values, and provides ready-to-copy YAML '
                                 'examples without requiring internet access.',
                      'demo_code': 'ansible-doc -s <module_name>',
                      'quick_tip': 'Replace <module_name> with the exact module you want to inspect (e.g. ping, '
                                   'command, copy, file).',
                      'syntax_breakdown': [   {'element': 'ansible-doc', 'role': 'Ansible documentation browser CLI'},
                                              {   'element': '-s',
                                                  'role': 'Snippet / short summary mode showing clean YAML parameter '
                                                          'skeleton'},
                                              {'element': 'ping', 'role': 'Name of the module to inspect'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.3\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'Ansible includes thousands of built-in modules for managing files, packages, services, '
                    'containers, and networks. Remembering all of their parameters by heart is impossible!\n'
                    '\n'
                    'Fortunately, Ansible ships with an offline documentation browser called `ansible-doc`.\n'
                    '\n'
                    'The Senior Systems Architect leaves a note:\n'
                    '> *"Before writing automation, inspect module schemas locally. Look up the snippet summary for '
                    'the `ping` module using `ansible-doc -s ping`."*',
        'solution_code': 'ansible-doc -s ping',
        'solution_type': 'command',
        'target': 'localhost',
        'tasks': [   "1. Query Ansible's internal documentation system from the CLI.",
                     '2. Inspect the snippet view of the ping module.',
                     '3. Review the available options and short synopsis.'],
        'title': 'Lesson 1.3: Module Manuals — Exploring Docs with ansible-doc',
        'validation_playbook': '---\n'
                               '- name: Validate 1.3\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify ansible-doc ping execution in audit log\n'
                               '      ansible.builtin.shell: |\n'
                               "        grep -q 'ansible-doc.*ping' /var/log/ansible.log || \\\n"
                               "        grep -q 'Try to connect to host' /var/log/ansible.log\n"
                               '      register: chk\n'
                               '      failed_when: chk.rc != 0\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### The `command` Module\n'
                       '\n'
                       'The `command` module is the default module in Ansible ad-hoc commands:\n'
                       '- Takes the command string via `-a "..."`\n'
                       '- Executes directly on remote nodes (without spawning a subshell `/bin/sh`)\n'
                       '- Safer than `shell` because it avoids quoting and injection hazards\n'
                       '\n'
                       '```bash\n'
                       'ansible all -m command -a "cat /etc/os-release"\n'
                       '```',
        'hints': [   {'level': 'Hint 1: The command Module', 'text': 'Use `-m command -a "cat /etc/os-release"`.'},
                     {'level': 'Hint 2: Execution', 'text': 'Run `ansible all -m command -a "cat /etc/os-release"`.'}],
        'id': 'l1-4-os-fingerprint',
        'inspect_cmd': 'cat /etc/os-release',
        'module': 'lvl1',
        'primer': {   'concept': 'The `ansible.builtin.command` module executes commands directly on remote systems '
                                 'via `execvp`. It is safer than the `shell` module because it does not process '
                                 'through `/bin/sh`, avoiding shell injection risks.',
                      'demo_code': 'ansible <target> -m command -a "<linux_command_and_args>"',
                      'quick_tip': 'Pass the exact command you want to run inside double quotes with the -a argument.',
                      'syntax_breakdown': [   {'element': 'ansible all', 'role': 'Target all cluster hosts'},
                                              {'element': '-m command', 'role': 'Invoke the command execution module'},
                                              {   'element': '-a "cat /etc/os-release"',
                                                  'role': 'Arguments passed directly to the remote binary'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.4\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'Now that connectivity is confirmed, the Lead Architect needs an inventory audit report:\n'
                    '> *"What exact Linux distribution and kernel version is running on each node in the fleet? Run '
                    '`cat /etc/os-release` across all nodes using the `command` module."*',
        'solution_code': 'ansible all -m command -a "cat /etc/os-release"',
        'solution_type': 'command',
        'target': 'all',
        'tasks': [   '1. Use the command module to run an arbitrary Linux command across all nodes.',
                     '2. Pass the arguments parameter (-a) to specify the command line to execute.',
                     '3. Observe how each node prints its unique distribution identity.'],
        'title': 'Lesson 1.4: OS Fingerprinting — Running Commands Fleet-Wide',
        'validation_playbook': '---\n'
                               '- name: Validate 1.4\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify os-release inspection in audit log\n'
                               '      ansible.builtin.shell: |\n'
                               "        grep -q 'node1-ubuntu' /var/log/ansible.log && \\\n"
                               "        grep -q 'NAME=' /var/log/ansible.log && \\\n"
                               "        grep -q 'VERSION_ID=' /var/log/ansible.log\n"
                               '      register: chk\n'
                               '      failed_when: chk.rc != 0\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### Checking Memory Footprints Ad-Hoc\n'
                       '\n'
                       'The `free -m` command provides quick visibility into RAM consumption:\n'
                       '```bash\n'
                       'ansible all -m command -a "free -m"\n'
                       '```\n'
                       'Notice how fast Ansible returns results because it runs over SSH in parallel forks (default 5 '
                       'concurrent connections).',
        'hints': [{'level': 'Hint 1: Command module', 'text': 'Run `ansible all -m command -a "free -m"`.'}],
        'id': 'l1-5-memory-check',
        'inspect_cmd': 'free -m',
        'module': 'lvl1',
        'primer': {   'concept': 'Ad-hoc inspection commands query live telemetry across dozens of hosts '
                                 'simultaneously using parallel SSH forks (default 5 concurrent connections).',
                      'demo_code': 'ansible <target> -m command -a "uptime"',
                      'quick_tip': 'You can execute any standard Linux diagnostic utility (like free -m, df -h, or '
                                   'uptime) via the command module.',
                      'syntax_breakdown': [   {'element': 'ansible all', 'role': 'Target all fleet nodes'},
                                              {'element': '-m command', 'role': 'Execute binary on remote targets'},
                                              {   'element': '-a "free -m"',
                                                  'role': 'Arguments to inspect RAM metrics in megabytes'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.5\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'A developer has asked to deploy a memory-intensive microservice. Before approving, the team needs '
                    'to know the available RAM across all cluster nodes.\n'
                    '\n'
                    '> *"Run `free -m` across all nodes to inspect memory totals and available headroom in '
                    'megabytes."*',
        'solution_code': 'ansible all -m command -a "free -m"',
        'solution_type': 'command',
        'target': 'all',
        'tasks': [   '1. Inspect available and utilized RAM across all fleet nodes in megabytes.',
                     '2. Verify memory metrics are successfully captured from every host.'],
        'title': 'Lesson 1.5: Resource Discovery — Querying Free Memory',
        'validation_playbook': '---\n'
                               '- name: Validate 1.5\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify free -m inspection in audit log\n'
                               '      ansible.builtin.shell: |\n'
                               "        grep -q 'node1-ubuntu' /var/log/ansible.log && \\\n"
                               "        grep -q 'Mem:' /var/log/ansible.log\n"
                               '      register: chk\n'
                               '      failed_when: chk.rc != 0\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### `command` vs `shell` Module\n'
                       '\n'
                       '- `command`: Safer and faster because it does not pass your string through `/bin/sh`. '
                       'Vulnerable to fewer escaping bugs, but **cannot** handle `|`, `>`, `<`, `&&`, or `;`.\n'
                       '- `shell`: Spawns `/bin/sh -c "<your_command>"` on the target. Required whenever you use pipes '
                       'or shell redirects.\n'
                       '\n'
                       '```bash\n'
                       'ansible all -m shell -a "uptime | awk \'{print \\$1}\'"\n'
                       '```',
        'hints': [   {'level': 'Hint 1: Use shell module', 'text': 'Specify `-m shell` instead of `-m command`.'},
                     {   'level': 'Hint 2: Escaping',
                         'text': 'Run `ansible all -m shell -a "uptime | awk \'{print \\$1}\'"`.'}],
        'id': 'l1-6-shell-pipes',
        'inspect_cmd': 'uptime',
        'module': 'lvl1',
        'primer': {   'concept': 'The `ansible.builtin.shell` module executes commands through `/bin/sh -c` on target '
                                 'machines. This enables shell pipelines (`|`), redirection (`>`, `>>`), chaining '
                                 '(`&&`), and environment variable evaluation.',
                      'demo_code': 'ansible <target> -m shell -a "<command> | grep <pattern>"',
                      'quick_tip': 'When piping to awk with column variables like $1, escape the dollar sign (\\$1) so '
                                   "your local bash doesn't expand it prematurely.",
                      'syntax_breakdown': [   {   'element': '-m shell',
                                                  'role': 'Execute command within /bin/sh subshell context'},
                                              {   'element': '| awk ...',
                                                  'role': 'Shell pipe routing stdout into awk for formatting'},
                                              {   'element': '\\$1',
                                                  'role': 'Escaped dollar sign to avoid early expansion on local '
                                                          'machine'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.6\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'In Lesson 1.5, you ran `free -m`. What if you wanted to pipe output into `awk` or `grep`?\n'
                    '\n'
                    'If you try running `ansible all -m command -a "uptime | awk \'{print $1}\'"`, the `command` '
                    'module will fail because it does NOT start a shell, so pipes (`|`) and redirects (`>`) are '
                    'treated as literal arguments!\n'
                    '\n'
                    'To use shell features like pipes, environment variables, or redirects, Ansible provides the '
                    '`shell` module.\n'
                    '\n'
                    '> *"Query the first word of the uptime command across all nodes using the `shell` module."*',
        'solution_code': 'ansible all -m shell -a "uptime | awk \'{print \\$1}\'"',
        'solution_type': 'command',
        'target': 'all',
        'tasks': [   '1. Understand the critical difference between command and shell modules.',
                     '2. Execute a command utilizing a shell pipeline to parse system output.',
                     '3. Extract and verify the current uptime timestamp from remote target nodes.'],
        'title': 'Lesson 1.6: Pipes & Shell Logic — Using the shell Module',
        'validation_playbook': '---\n'
                               '- name: Validate 1.6\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify shell pipe execution in audit log\n'
                               '      ansible.builtin.shell: |\n'
                               "        grep -q 'node1-ubuntu' /var/log/ansible.log && \\\n"
                               "        grep -qE '[0-9]{2}:[0-9]{2}|up' /var/log/ansible.log\n"
                               '      register: chk\n'
                               '      failed_when: chk.rc != 0\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### The `setup` Module & Ansible Facts\n'
                       '\n'
                       'Whenever an Ansible playbook runs with `gather_facts: true`, it automatically calls the '
                       '`setup` module under the hood:\n'
                       '- `ansible_distribution`: OS family (e.g. `Ubuntu`, `Debian`, `AlmaLinux`, `Alpine`)\n'
                       '- `ansible_distribution_major_version`: Major version number (e.g. `24`, `12`, `9`, `3`)\n'
                       '- `ansible_default_ipv4.address`: Default IP address\n'
                       '- `ansible_memtotal_mb`: Total system RAM\n'
                       '\n'
                       '```bash\n'
                       'ansible node1-ubuntu -m setup -a "filter=ansible_distribution*"\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Setup module syntax',
                         'text': 'Run `ansible <node> -m setup -a "filter=<pattern>"`.'},
                     {   'level': 'Hint 2: Filter value',
                         'text': 'Run `ansible node1-ubuntu -m setup -a "filter=ansible_distribution*"`.'}],
        'id': 'l1-7-fact-gathering',
        'inspect_cmd': "ansible node1-ubuntu -m setup -a 'filter=ansible_distribution*'",
        'module': 'lvl1',
        'primer': {   'concept': "Ansible's `setup` module automatically interrogates remote hosts and returns "
                                 'detailed JSON telemetry about CPU, memory, disks, network interfaces, and OS '
                                 'distribution.',
                      'demo_code': 'ansible <target_host> -m setup -a "filter=<fact_pattern*>"',
                      'quick_tip': 'Use wildcards like filter=ansible_distribution* to retrieve OS family, release, '
                                   'and version details.',
                      'syntax_breakdown': [   {   'element': '-m setup',
                                                  'role': "Invokes Ansible's fact discovery engine"},
                                              {   'element': 'filter=...',
                                                  'role': 'Wildcard pattern limiting output to relevant fact keys'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.7\n'
                          '  hosts: node1-ubuntu\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'In Lesson 1.4, you read `/etc/os-release` manually. But Ansible actually has a built-in discovery '
                    'engine that automatically discovers hundreds of hardware, network, and OS facts!\n'
                    '\n'
                    'This engine is powered by the `setup` module.\n'
                    '\n'
                    '> *"Query the setup engine on `node1-ubuntu` and filter facts starting with '
                    '`ansible_distribution*` to retrieve the OS distribution name and major version."*',
        'solution_code': 'ansible node1-ubuntu -m setup -a "filter=ansible_distribution*"',
        'solution_type': 'command',
        'target': 'node1-ubuntu',
        'tasks': [   '1. Interrogate the setup engine on node1-ubuntu.',
                     '2. Apply a filter pattern to retrieve ansible_distribution facts.',
                     '3. Verify structured JSON facts are returned.'],
        'title': 'Lesson 1.7: Fact Gathering — Querying the Setup Engine',
        'validation_playbook': '---\n'
                               '- name: Validate 1.7\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify setup filter inspection in audit log\n'
                               '      ansible.builtin.shell: |\n'
                               "        grep -q 'node1-ubuntu | SUCCESS' /var/log/ansible.log && \\\n"
                               '        grep -q \'"ansible_distribution": "Ubuntu"\' /var/log/ansible.log\n'
                               '      register: chk\n'
                               '      failed_when: chk.rc != 0\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### Auditing with `stat`\n'
                       '\n'
                       'The `stat` module returns structured file metadata:\n'
                       '- `stat.exists`: boolean (`true` or `false`)\n'
                       '- `stat.pw_name`: owner\n'
                       '- `stat.mode`: octal permissions (`0644`)\n'
                       '\n'
                       '```bash\n'
                       'ansible all -m stat -a "path=/etc/hosts"\n'
                       '```',
        'hints': [{'level': 'Hint 1: stat module', 'text': 'Run `ansible all -m stat -a "path=/etc/hosts"`.'}],
        'id': 'l1-8-file-stat',
        'inspect_cmd': 'stat /etc/hosts',
        'module': 'lvl1',
        'primer': {   'concept': 'The `stat` module retrieves status and metadata about a remote file or directory, '
                                 'returning structured properties like existence (`exists: true`), permissions '
                                 '(`mode`), owner (`pw_name`), and file size.',
                      'demo_code': 'ansible <target> -m stat -a "path=/path/to/target_file"',
                      'quick_tip': 'The stat module checks if a file exists, its file size, owner, and permissions '
                                   'without altering anything.',
                      'syntax_breakdown': [   {'element': '-m stat', 'role': 'Query file attributes and existence'},
                                              {   'element': 'path=/path',
                                                  'role': 'Target file or directory to inspect on remote nodes'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.8\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'Before modifying files on servers, automated playbooks should check whether files exist and what '
                    'their current permissions are.\n'
                    '\n'
                    'The `stat` module retrieves file metadata on remote systems (similar to `stat(2)` syscall).\n'
                    '\n'
                    '> *"Audit `/etc/hosts` across all nodes using the `stat` module."*',
        'solution_code': 'ansible all -m stat -a "path=/etc/hosts"',
        'solution_type': 'command',
        'target': 'all',
        'tasks': [   '1. Inspect file metadata for /etc/hosts across all nodes.',
                     '2. Confirm attributes like existence, permissions, and ownership are returned.'],
        'title': 'Lesson 1.8: File Auditing — The stat Module',
        'validation_playbook': '---\n'
                               '- name: Validate 1.8\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify stat inspection in audit log\n'
                               '      ansible.builtin.shell: |\n'
                               "        grep -q 'node1-ubuntu | SUCCESS' /var/log/ansible.log && \\\n"
                               '        (grep -q \'"exists": true\' /var/log/ansible.log || grep -q \'"stat":\' '
                               '/var/log/ansible.log)\n'
                               '      register: chk\n'
                               '      failed_when: chk.rc != 0\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### The `file` Module and `state=touch`\n'
                       '\n'
                       'The `ansible.builtin.file` module is declarative:\n'
                       '- `path`: Target file or directory\n'
                       '- `state=touch`: If the file does not exist, create it. If it exists, update its mtime (like '
                       'Linux `touch`).\n'
                       '\n'
                       '```bash\n'
                       'ansible all -m file -a "path=/tmp/audit.log state=touch"\n'
                       '```\n'
                       'Notice the color in terminal:\n'
                       '- **Green**: `SUCCESS` (no state altered)\n'
                       '- **Yellow**: `CHANGED` (target state modified)',
        'hints': [   {   'level': 'Hint 1: The file Module',
                         'text': 'Use `file` with `state=touch` to ensure a file timestamp exists: `ansible <target> '
                                 '-m file -a "path=<file> state=touch"`.'},
                     {   'level': 'Hint 2: Command Syntax',
                         'text': 'Run `ansible all -m file -a "path=/tmp/audit.log state=touch"`.'}],
        'id': 'l1-9-touch-marker',
        'inspect_cmd': 'ls -l /tmp/audit.log',
        'module': 'lvl1',
        'primer': {   'concept': 'The `ansible.builtin.file` module declaratively manages file attributes, symlinks, '
                                 'directories, and timestamps. Setting `state=touch` creates an empty file if missing '
                                 'or updates its modification time.',
                      'demo_code': 'ansible <target> -m file -a "path=/path/to/marker.flag state=touch"',
                      'quick_tip': 'state=touch creates an empty file if missing or updates its timestamp if it '
                                   'already exists.',
                      'syntax_breakdown': [   {'element': '-m file', 'role': 'File and filesystem management module'},
                                              {'element': 'path=...', 'role': 'Target file path'},
                                              {   'element': 'state=touch',
                                                  'role': 'Ensures file exists and updates mtime'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.9\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove audit file if present\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/audit.log\n'
                          '        state: absent\n',
        'scenario': 'In Lesson 1.8, you checked file existence with `stat`. Now, you will make your first actual state '
                    'modification across the cluster!\n'
                    '\n'
                    'DataForge security compliance requires placing an audit marker file `/tmp/audit.log` on every '
                    'server to register when this node was audited.\n'
                    '\n'
                    '> *"Use the `file` module with `state=touch` to create or update `/tmp/audit.log` across all 6 '
                    'nodes."*',
        'solution_code': 'ansible all -m file -a "path=/tmp/audit.log state=touch"',
        'solution_type': 'command',
        'target': 'all',
        'tasks': [   '1. Ensure an audit log marker /tmp/audit.log exists across all fleet nodes.',
                     '2. Confirm the state change is registered with a changed status.'],
        'title': 'Lesson 1.9: Touching First Marker — Dropping an Audit Timestamp',
        'validation_playbook': '---\n'
                               '- name: Validate 1.9\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check /tmp/audit.log exists\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/audit.log\n'
                               '      register: audit_st\n'
                               '    - name: Assert audit marker is present\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - audit_st.stat.exists == true\n',
        'xp': 50},
    {   'difficulty': 'Beginner',
        'explanation': '### Ad-Hoc File Copying\n'
                       '\n'
                       "The `copy` module is one of Ansible's most powerful primitives:\n"
                       '```bash\n'
                       'ansible debian -m copy -a "content=\'active_window=2026\\n\' dest=/etc/dataforge_maintenance"\n'
                       '```\n'
                       'It ensures idempotency: if `/etc/dataforge_maintenance` already has that exact content, '
                       'Ansible reports `SUCCESS` (green) and does NOT touch disk write timestamps.',
        'hints': [   {   'level': 'Hint 1: Ad-hoc copy module',
                         'text': 'Use `copy` with `content` and `dest`: `ansible <group> -m copy -a "content=\'...\' '
                                 'dest=..."`.'},
                     {   'level': 'Hint 2: The Command',
                         'text': 'Run `ansible debian -m copy -a "content=\'active_window=2026\\n\' '
                                 'dest=/etc/dataforge_maintenance"`.'}],
        'id': 'l1-10-fleet-distribution',
        'inspect_cmd': "cat /etc/dataforge_maintenance 2>/dev/null || echo 'Not present'",
        'module': 'lvl1',
        'primer': {   'concept': 'The `copy` module transfers files or inline text strings to remote machines. Using '
                                 'the `content` parameter, you can write file contents directly without needing a '
                                 'source file on the control machine.',
                      'demo_code': 'ansible <target_group> -m copy -a "content=\'<payload_string>\\n\' '
                                   'dest=/path/to/file"',
                      'quick_tip': 'Make sure to enclose the whole argument string in double quotes and inner content '
                                   'in single quotes to avoid quoting issues.',
                      'syntax_breakdown': [   {   'element': 'ansible debian',
                                                  'role': 'Target the debian group in inventory'},
                                              {'element': '-m copy', 'role': 'Invoke the copy module'},
                                              {   'element': "content='...'",
                                                  'role': 'Inline text string to write into destination'},
                                              {   'element': 'dest=/path',
                                                  'role': 'Absolute remote file destination path'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 1.10\n'
                          '  hosts: debian\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove maintenance flag\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/dataforge_maintenance\n'
                          '        state: absent\n',
        'scenario': 'In Lesson 1.9, you created an empty file with `file: state=touch`. But in production incidents, '
                    'you frequently need to push config snippets, environment flags, or license tokens immediately '
                    'across hosts.\n'
                    '\n'
                    'The `copy` module allows pushing inline content directly from your command line without needing '
                    'local files!\n'
                    '\n'
                    'Your Systems Lead asks:\n'
                    '> *"Distribute an emergency maintenance flag `/etc/dataforge_maintenance` containing '
                    '`active_window=2026` across all Debian nodes."*',
        'solution_code': 'ansible debian -m copy -a "content=\'active_window=2026\\n\' '
                         'dest=/etc/dataforge_maintenance"',
        'solution_type': 'command',
        'target': 'debian',
        'tasks': [   '1. Target the Debian server slice.',
                     '2. Use the copy module with content and dest parameters to write /etc/dataforge_maintenance.',
                     '3. Confirm that the file is successfully placed on remote nodes.'],
        'title': 'Lesson 1.10: Fleet Distribution — Pushing Content with the copy Module',
        'validation_playbook': '---\n'
                               '- name: Validate 1.10\n'
                               '  hosts: debian\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check /etc/dataforge_maintenance exists\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /etc/dataforge_maintenance\n'
                               '      register: st\n'
                               '    - name: Check file contents\n'
                               '      ansible.builtin.command: cat /etc/dataforge_maintenance\n'
                               '      register: contents\n'
                               '      when: st.stat.exists\n'
                               '    - name: Assert content matches\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - st.stat.exists\n'
                               '          - "\'active_window=2026\' in contents.stdout"\n',
        'xp': 50},
    {   'difficulty': 'Intermediate',
        'explanation': '### Ad-Hoc Incident Response Patterns\n'
                       '\n'
                       'In high-pressure SRE incident response, ad-hoc commands provide instantaneous targeted '
                       'remediation without needing to author a playbook:\n'
                       '1. **Targeted Purge (`file: state=absent`)**:\n'
                       '```bash\n'
                       'ansible alpine -m file -a "path=/tmp/.malware_beacon state=absent"\n'
                       '```\n'
                       '2. **Instant State Alignment (`copy: content=...`)**:\n'
                       '```bash\n'
                       'ansible debian -m copy -a "content=\'DataForge Fleet Node\' dest=/etc/motd"\n'
                       '```\n'
                       '3. **Emergency Process Termination (`shell: pkill ...`)**:\n'
                       '```bash\n'
                       'ansible rhel -m shell -a "pkill sleep || true"\n'
                       '```\n'
                       'You have successfully completed **Level 1** and defeated your first SRE Incident!',
        'hints': [   {   'level': 'Hint 1: Targeting Groups',
                         'text': 'Remember group targeting: use `ansible alpine ...`, `ansible debian ...`, and '
                                 '`ansible rhel ...` to target specific slices without affecting the whole fleet.'},
                     {   'level': 'Hint 2: Exact Ad-Hoc Commands',
                         'text': 'Run:\n'
                                 '1) `ansible alpine -m file -a "path=/tmp/.malware_beacon state=absent"`\n'
                                 '2) `ansible debian -m copy -a "content=\'DataForge Fleet Node\' dest=/etc/motd"`\n'
                                 '3) `ansible rhel -m shell -a "pkill sleep || true"`'}],
        'id': 'l1-11-fleet-cleanup',
        'inspect_cmd': "ansible all -m shell -a 'ls -l /tmp/.malware_beacon 2>/dev/null; cat /etc/motd 2>/dev/null; "
                       "pgrep -x sleep || true' || true",
        'module': 'lvl1',
        'primer': {   'concept': 'SRE incident response demands chaining ad-hoc tools under pressure. In this '
                                 'challenge, apply group targeting (`alpine`, `debian`, `rhel`), removal (`file: '
                                 'state=absent`), content restoration (`copy: content=...`), and process termination '
                                 '(`shell: pkill ...`).',
                      'demo_code': '# Triage Blueprint Template:\n'
                                   'ansible <group1> -m file -a "path=<bad_file> state=absent"\n'
                                   'ansible <group2> -m copy -a "content=\'<authorized_text>\\n\' dest=/path/to/file"\n'
                                   'ansible <group3> -m shell -a "pkill <process_name> || true"',
                      'quick_tip': 'Execute one ad-hoc remediation per target slice and inspect the output status '
                                   'colors (yellow = changed, green = success).',
                      'syntax_breakdown': [   {   'element': 'ansible <group>',
                                                  'role': 'Target exact server slice (alpine, debian, rhel)'},
                                              {'element': 'state=absent', 'role': 'Idempotent file deletion'},
                                              {   'element': 'copy: content=...',
                                                  'role': 'Instant file recreation with authorized payload'},
                                              {   'element': 'shell: pkill ...',
                                                  'role': 'Emergency process termination with || true fallback'}]},
        'reset_playbook': '---\n'
                          '- name: Reset Incident 1042\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Seed malware beacon on alpine\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/.malware_beacon\n'
                          '        state: touch\n'
                          "      when: inventory_hostname == 'node6-alpine'\n"
                          '    - name: Deface debian motd\n'
                          '      ansible.builtin.copy:\n'
                          '        content: "DEFACED_BREACH"\n'
                          '        dest: /etc/motd\n'
                          "      when: inventory_hostname in ['node2-debian', 'node3-debian13']\n"
                          '    - name: Spawn rogue process on almalinux\n'
                          '      ansible.builtin.shell: "nohup sleep 99999 >/dev/null 2>&1 &"\n'
                          "      when: inventory_hostname == 'node4-almalinux'\n",
        'scenario': '🚨 **SEVERITY 3 ALERT: UNKNOWN ACTIVITY DETECTED ACROSS INHERITED FLEET**\n'
                    'DataForge SRE telemetry detected 3 anomalies across the cluster:\n'
                    '1. **Host `node6-alpine`**: An unauthorized payload file `/tmp/.malware_beacon` was detected.\n'
                    '2. **Host `node2-debian`**: The SSH `/etc/motd` banner has been altered to `DEFACED_BREACH`.\n'
                    '3. **RHEL cluster (`node4-almalinux`)**: A rogue background task is spinning CPU in the '
                    'background.\n'
                    '\n'
                    'The Incident Commander instructs:\n'
                    '> *"Using ONLY Ansible ad-hoc commands, hunt down the anomalies across all nodes:*\n'
                    '> *1. Eradicate `/tmp/.malware_beacon` on `alpine` using `file: state=absent`.*\n'
                    '> *2. Restore `/etc/motd` on `debian` to `DataForge Fleet Node` using `copy`.*\n'
                    '> *3. Terminate any rogue `sleep 99999` processes on `rhel` hosts using `shell: pkill sleep || '
                    'true`.*\n'
                    '> *Verify all targets return clean state before closing this ticket!"*',
        'setup_playbook': '---\n'
                          '- name: Setup Incident 1042\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Seed malware beacon on alpine\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/.malware_beacon\n'
                          '        state: touch\n'
                          "      when: inventory_hostname == 'node6-alpine'\n"
                          '    - name: Deface debian motd\n'
                          '      ansible.builtin.copy:\n'
                          '        content: "DEFACED_BREACH"\n'
                          '        dest: /etc/motd\n'
                          "      when: inventory_hostname in ['node2-debian', 'node3-debian13']\n"
                          '    - name: Spawn rogue process on almalinux\n'
                          '      ansible.builtin.shell: "nohup sleep 99999 >/dev/null 2>&1 &"\n'
                          "      when: inventory_hostname == 'node4-almalinux'\n",
        'solution_code': 'ansible alpine -m file -a "path=/tmp/.malware_beacon state=absent" && ansible debian -m copy '
                         '-a "content=\'DataForge Fleet Node\' dest=/etc/motd" && ansible rhel -m shell -a "pkill '
                         'sleep || true"',
        'solution_type': 'command',
        'target': 'all',
        'tasks': [   '1. Eradicate /tmp/.malware_beacon on alpine using file: state=absent.',
                     "2. Restore /etc/motd on debian to DataForge Fleet Node using copy.",
                     '3. Terminate any rogue sleep 99999 processes on rhel hosts using shell: pkill sleep || true.'],
        'title': 'Lesson 1.11: MINI-BOSS: Incident #1042 — Operation Ghost Hunter',
        'validation_playbook': '---\n'
                               '- name: Validate Incident 1042\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check malware beacon on alpine\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/.malware_beacon\n'
                               '      register: beacon_st\n'
                               "      when: inventory_hostname == 'node6-alpine'\n"
                               '    - name: Assert beacon absent\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - not beacon_st.stat.exists\n'
                               "      when: inventory_hostname == 'node6-alpine'\n"
                               '\n'
                               '    - name: Check debian motd\n'
                               '      ansible.builtin.command: cat /etc/motd\n'
                               '      register: motd_res\n'
                               "      when: inventory_hostname in ['node2-debian', 'node3-debian13']\n"
                               '    - name: Assert debian motd restored\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'DataForge\' in motd_res.stdout"\n'
                               "      when: inventory_hostname in ['node2-debian', 'node3-debian13']\n"
                               '\n'
                               '    - name: Check rogue process dead on almalinux\n'
                               '      ansible.builtin.shell: "pgrep -x sleep || true"\n'
                               '      register: proc_res\n'
                               "      when: inventory_hostname == 'node4-almalinux'\n"
                               '    - name: Assert rogue process terminated\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - proc_res.stdout == ""\n'
                               "      when: inventory_hostname == 'node4-almalinux'\n",
        'xp': 100}]

