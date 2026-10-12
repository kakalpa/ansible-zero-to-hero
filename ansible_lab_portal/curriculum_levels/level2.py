# Level 2: Automation Blueprint — Declarative Playbooks (Lessons 2.1 to 2.13)

LEVEL2_EXERCISES = [   {   'difficulty': 'Beginner',
        'explanation': '### Anatomy of an Ansible Playbook\n'
                       'A playbook contains one or more **plays**. Each play maps a group of hosts to a series of '
                       'tasks:\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Verify Cluster Readiness\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Ping all nodes\n'
                       '      ansible.builtin.ping:\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/ping.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Playbook Skeleton',
                         'text': 'Every playbook starts with `---\\n- name: <description>\\n  hosts: all\\n  '
                                 'gather_facts: false\\n  tasks:\\n    - name: <task>\\n      ansible.builtin.ping:'},
                     {   'level': 'Hint 2: Execution',
                         'text': 'Run `ansible-playbook /ansible/ping.yml` in the terminal.'}],
        'id': 'l2-1-first-playbook',
        'inspect_cmd': 'ansible-playbook /ansible/ping.yml --syntax-check',
        'module': 'lvl2',
        'primer': {   'concept': 'Ansible Playbooks are declarative YAML files describing the desired state of remote '
                                 'systems. Unlike imperative shell scripts, playbooks express *what* systems should '
                                 'look like, allowing Ansible to calculate the minimal state changes required.',
                      'demo_code': '---\n'
                                   '- name: Example Connectivity Verification\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Test responsiveness\n'
                                   '      ansible.builtin.ping:\n',
                      'quick_tip': "Replace <target_hosts> with the group or pattern (e.g. 'all') required by your "
                                   'mission ticket.',
                      'syntax_breakdown': [   {'element': '---', 'role': 'Standard YAML document start marker'},
                                              {   'element': 'hosts: all',
                                                  'role': 'Target hosts or inventory groups for this play'},
                                              {   'element': 'gather_facts: false',
                                                  'role': 'Skips automatic setup module interrogation for speed'},
                                              {   'element': 'tasks:',
                                                  'role': 'Ordered list of automation actions executed sequentially'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.1\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'Welcome to **Level 2: Automation Blueprint**! Ad-hoc commands are great for quick recon, but '
                    'enterprise infrastructure requires auditable, version-controlled playbooks.\n'
                    '\n'
                    'Your task from the Platform Engineering Team:\n'
                    '> *"Create your very first YAML playbook `/ansible/ping.yml`. It must target `all` hosts, set '
                    '`gather_facts: false` for speed, and execute the `ansible.builtin.ping` module."*\n'
                    '\n'
                    'Open `/ansible/ping.yml` in the editor, write the play, and run it with `ansible-playbook '
                    '/ansible/ping.yml`.',
        'solution_code': '---\n'
                         '- name: Verify Cluster Readiness\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Ping all nodes\n'
                         '      ansible.builtin.ping:\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/ping.yml',
        'tasks': [   '1. Author the /ansible/ping.yml playbook targeting all fleet nodes.',
                     '2. Ensure gather_facts is set to false to optimize execution speed.',
                     '3. Invoke ansible.builtin.ping within the tasks list.',
                     '4. Execute the playbook using the ansible-playbook CLI.'],
        'title': 'Lesson 2.1: First Playbook — Converting Ad-Hoc to Declarative YAML',
        'validation_playbook': '---\n'
                               '- name: Validate 2.1\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify playbook syntax\n'
                               '      ansible.builtin.command: ansible-playbook /ansible/ping.yml --syntax-check\n'
                               '      register: syn_chk\n'
                               '      failed_when: syn_chk.rc != 0\n'
                               '\n'
                               '    - name: Execute ping.yml to verify cluster success\n'
                               '      ansible.builtin.command: ansible-playbook /ansible/ping.yml\n'
                               '      register: run_chk\n'
                               '      failed_when: run_chk.rc != 0\n',
        'xp': 100},
    {   'difficulty': 'Beginner',
        'explanation': '### The `debug` Module\n'
                       'The `debug` module is safe and produces 0 state changes (`ok` status):\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Output Diagnostic Message\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Print welcome banner\n'
                       '      ansible.builtin.debug:\n'
                       '        msg: "DataForge Automation Active"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/debug_msg.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: debug module syntax',
                         'text': 'Under tasks, use:\\n  ansible.builtin.debug:\\n    msg: "DataForge Automation '
                                 'Active"'},
                     {   'level': 'Hint 2: Execution',
                         'text': 'Run `ansible-playbook /ansible/debug_msg.yml` in the terminal.'}],
        'id': 'l2-2-debug-module',
        'inspect_cmd': 'ansible-playbook /ansible/debug_msg.yml',
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.debug` module prints statements during execution. It is '
                                 'essential for troubleshooting playbook flow, verifying variable values, and '
                                 'displaying operational notices without altering target systems.',
                      'demo_code': '---\n'
                                   '- name: Display Diagnostic Information\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Print custom message to terminal\n'
                                   '      ansible.builtin.debug:\n'
                                   '        msg: "<your_diagnostic_message>"\n',
                      'quick_tip': "debug tasks never alter system state and always return 'ok' (green).",
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.debug:',
                                                  'role': 'Module for printing text or variables'},
                                              {   'element': 'msg: "..."',
                                                  'role': 'String message printed to the console output for each '
                                                          'host'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.2\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'Before modifying server files or user accounts, engineers test playbook logic and print '
                    'diagnostic messages to the terminal.\n'
                    '\n'
                    'The `ansible.builtin.debug` module prints messages during playbook execution.\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/debug_msg.yml` targeting `all` nodes. Add a task using '
                    '`ansible.builtin.debug` to print the exact message `DataForge Automation Active`."*\n'
                    '\n'
                    'Run your playbook and observe how output is reported per host.',
        'solution_code': '---\n'
                         '- name: Output Diagnostic Message\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Print welcome banner\n'
                         '      ansible.builtin.debug:\n'
                         '        msg: "DataForge Automation Active"\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/debug_msg.yml',
        'tasks': [   '1. Author /ansible/debug_msg.yml targeting all hosts.',
                     '2. Use ansible.builtin.debug with parameter msg.',
                     "3. Set msg to 'DataForge Automation Active'.",
                     '4. Run ansible-playbook /ansible/debug_msg.yml.'],
        'title': 'Lesson 2.2: Hello Automation — Printing Diagnostic Messages with debug',
        'validation_playbook': '---\n'
                               '- name: Validate 2.2\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Execute debug_msg.yml\n'
                               '      ansible.builtin.command: ansible-playbook /ansible/debug_msg.yml\n'
                               '      register: dbg_res\n'
                               "      failed_when: dbg_res.rc != 0 or 'DataForge Automation Active' not in "
                               'dbg_res.stdout\n',
        'xp': 100},
    {   'difficulty': 'Beginner',
        'explanation': '### Idempotent File Management with `copy`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Deploy Standard MOTD\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Update /etc/motd\n'
                       '      ansible.builtin.copy:\n'
                       '        content: "Authorized Access Only - DataForge Infrastructure\n'
                       '"\n'
                       '        dest: /etc/motd\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/motd.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: copy module in YAML',
                         'text': 'tasks:\\n  - name: Set MOTD\\n    ansible.builtin.copy:\\n      content: "Authorized '
                                 'Access Only - DataForge Infrastructure\\n"\\n      dest: /etc/motd'}],
        'id': 'l2-3-motd-banner',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/motd'",
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.copy` module in playbooks manages remote file contents '
                                 'idempotently. If the remote file already matches the declared content, Ansible skips '
                                 'the task (`ok`), preventing unnecessary disk writes.',
                      'demo_code': '---\n'
                                   '- name: Deploy Standard File\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Write configuration file\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/target_file\n'
                                   '        content: "<required_file_content>\\n"\n'
                                   "        mode: '0644'\n",
                      'quick_tip': 'Always end file content strings with \\n to ensure standard POSIX newline '
                                   'formatting.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.copy:',
                                                  'role': 'Module for placing files or text'},
                                              {   'element': 'content: "..."',
                                                  'role': 'Inline text payload to write into destination'},
                                              {   'element': 'dest: /etc/motd',
                                                  'role': 'Target file destination path on remote nodes'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.3\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Wipe motd\n'
                          '      ansible.builtin.copy:\n'
                          '        content: "Default"\n'
                          '        dest: /etc/motd\n',
        'scenario': "In Lesson 2.2, you printed a debug message. Now let's create actual remote files declaratively!\n"
                    '\n'
                    'Corporate policy requires standardizing the `/etc/motd` banner across all servers to display:\n'
                    '`Authorized Access Only - DataForge Infrastructure`\n'
                    '\n'
                    'Author `/ansible/motd.yml` targeting `all` nodes. Use `ansible.builtin.copy` with `content` and '
                    '`dest: /etc/motd`.',
        'solution_code': '---\n'
                         '- name: Deploy Standard MOTD\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Update /etc/motd\n'
                         '      ansible.builtin.copy:\n'
                         '        content: "Authorized Access Only - DataForge Infrastructure\n'
                         '"\n'
                         '        dest: /etc/motd\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/motd.yml',
        'tasks': [   '1. Create /ansible/motd.yml targeting all hosts.',
                     '2. Use ansible.builtin.copy to deploy /etc/motd.',
                     "3. Ensure the content includes 'Authorized Access Only - DataForge Infrastructure'.",
                     '4. Run ansible-playbook /ansible/motd.yml and verify green/yellow status.'],
        'title': 'Lesson 2.3: Fleet Consistency — Deploying MOTD with the copy Module',
        'validation_playbook': '---\n'
                               '- name: Validate 2.3\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check /etc/motd content\n'
                               '      ansible.builtin.command: cat /etc/motd\n'
                               '      register: motd_res\n'
                               '    - name: Assert MOTD banner matches\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'Authorized Access Only - DataForge Infrastructure\' in '
                               'motd_res.stdout"\n',
        'xp': 100},
    {   'difficulty': 'Beginner',
        'explanation': '### Surgical Editing with `lineinfile`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Ensure Host Resolution\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Add internal auth host entry\n'
                       '      ansible.builtin.lineinfile:\n'
                       '        path: /etc/hosts\n'
                       '        line: "192.168.1.10 auth.dataforge.internal"\n'
                       '        unsafe_writes: true\n'
                       '```\n'
                       '> **💡 SRE Note (Container Bind Mounts)**: In containerized fleets (Docker/Kubernetes), `/etc/hosts` is a kernel bind mount. Ansible\'s default atomic rename fails with `[Errno 16] Device or resource busy`. Setting `unsafe_writes: true` instructs Ansible to write directly into the file.\n\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/hosts.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: lineinfile syntax',
                         'text': 'tasks:\\n  - name: Add DNS entry\\n    ansible.builtin.lineinfile:\\n      path: '
                                 '/etc/hosts\\n      line: "192.168.1.10 auth.dataforge.internal"\\n      unsafe_writes: true'},
                     {   'level': 'Hint 2: Device or resource busy',
                         'text': 'Because /etc/hosts is a container bind mount, include `unsafe_writes: true` under `ansible.builtin.lineinfile`.'}],
        'id': 'l2-4-lineinfile-hosts',
        'inspect_cmd': "ansible all -m command -a 'grep auth.dataforge /etc/hosts'",
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.lineinfile` module searches for a specific line in a text file. '
                                 'If the line is not found, it appends it. If it is found, no change is made. It can '
                                 'also replace lines matching a regex pattern. In container fleets where files like `/etc/hosts` are bind-mounted, `unsafe_writes: true` is required to allow in-place file modification.',
                      'demo_code': '---\n'
                                   '- name: Manage Single Configuration Line\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Ensure configuration entry is present\n'
                                   '      ansible.builtin.lineinfile:\n'
                                   '        path: /path/to/config_file\n'
                                   '        line: "<exact_line_to_ensure>"\n'
                                   '        unsafe_writes: true\n',
                      'quick_tip': "In Docker containers, /etc/hosts is a bind mount. Add 'unsafe_writes: true' so Ansible writes directly without atomic rename errors.",
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.lineinfile:',
                                                  'role': 'Module for granular single-line edits'},
                                              {'element': 'path: /etc/hosts', 'role': 'Target file to modify'},
                                              {   'element': 'line: "..."',
                                                  'role': 'Exact line to ensure is present in the file'},
                                              {   'element': 'unsafe_writes: true',
                                                  'role': 'Enables in-place write for container bind-mounted files (/etc/hosts)'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.4\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove auth entry\n'
                          '      ansible.builtin.lineinfile:\n'
                          '        path: /etc/hosts\n'
                          '        line: "192.168.1.10 auth.dataforge.internal"\n'
                          '        state: absent\n'
                          '        unsafe_writes: true\n',
        'scenario': 'The `copy` module overwrites entire files. But what if you only need to ensure a single line is '
                    'present in an existing configuration file without destroying existing contents?\n'
                    '\n'
                    'The `ansible.builtin.lineinfile` module ensures a specific line exists in a file. If the line is '
                    'already present, it does nothing!\n'
                    '\n'
                    'DataForge needs an internal DNS fallback entry added to `/etc/hosts` on all servers:\n'
                    '`192.168.1.10 auth.dataforge.internal`\n'
                    '\n'
                    '*(Note: In container fleets where `/etc/hosts` is bind-mounted, remember to include `unsafe_writes: true`)*.\n'
                    '\n'
                    'Author `/ansible/hosts.yml` to append this line to `/etc/hosts`.',
        'solution_code': '---\n'
                         '- name: Ensure Host Resolution\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Add internal auth host entry\n'
                         '      ansible.builtin.lineinfile:\n'
                         '        path: /etc/hosts\n'
                         '        line: "192.168.1.10 auth.dataforge.internal"\n'
                         '        unsafe_writes: true\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/hosts.yml',
        'tasks': [   '1. Create /ansible/hosts.yml targeting all nodes.',
                     '2. Use ansible.builtin.lineinfile targeting path /etc/hosts.',
                     "3. Set line to '192.168.1.10 auth.dataforge.internal'.",
                     '4. Run ansible-playbook /ansible/hosts.yml.'],
        'title': 'Lesson 2.4: Safe Line Appends — Editing Files with lineinfile',
        'validation_playbook': '---\n'
                               '- name: Validate 2.4\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify entry in /etc/hosts\n'
                               '      ansible.builtin.command: grep "192.168.1.10 auth.dataforge.internal" /etc/hosts\n'
                               '      register: grep_res\n'
                               '      failed_when: grep_res.rc != 0\n',
        'xp': 100},
    {   'difficulty': 'Beginner',
        'explanation': '### The `blockinfile` Module\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Manage Security Banner Block\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Insert banner block in /etc/issue.net\n'
                       '      ansible.builtin.blockinfile:\n'
                       '        path: /etc/issue.net\n'
                       '        create: true\n'
                       '        block: |\n'
                       '          Authorized Access Only.\n'
                       '          All activities are monitored and logged.\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/block_config.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: blockinfile syntax',
                         'text': 'ansible.builtin.blockinfile:\\n  path: /etc/issue.net\\n  create: true\\n  block: '
                                 '|\\n    Authorized Access Only.\\n    All activities are monitored and logged.'}],
        'id': 'l2-5-blockinfile',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/issue.net'",
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.blockinfile` module manages a contiguous multi-line block '
                                 'within an existing file. It demarcates the block with special marker comments, '
                                 'allowing Ansible to update or delete the exact block later without disturbing the '
                                 'rest of the file.',
                      'demo_code': '---\n'
                                   '- name: Manage Multi-Line Configuration Stanza\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Insert managed block of lines\n'
                                   '      ansible.builtin.blockinfile:\n'
                                   '        path: /path/to/file\n'
                                   '        create: true\n'
                                   '        block: |\n'
                                   '          <first line of block>\n'
                                   '          <second line of block>\n',
                      'quick_tip': 'The pipe symbol (|) in YAML preserves literal newlines in multi-line text blocks.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.blockinfile:',
                                                  'role': 'Module for managing multi-line text blocks'},
                                              {   'element': 'path: /etc/issue.net',
                                                  'role': 'Destination file to modify or create'},
                                              {   'element': 'create: true',
                                                  'role': 'Creates the file if it does not already exist'},
                                              {   'element': 'block: |',
                                                  'role': 'YAML literal block scalar preserving line breaks'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.5\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove issue.net\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/issue.net\n'
                          '        state: absent\n',
        'scenario': 'Single-line edits with `lineinfile` are ideal for single values, but managing multi-line '
                    'configuration blocks (such as firewall rules, banner disclaimers, or SSH options) requires '
                    '`blockinfile`.\n'
                    '\n'
                    '`blockinfile` inserts a marked multi-line block into an existing file surrounded by comments:\n'
                    '`# BEGIN ANSIBLE MANAGED BLOCK` ... `# END ANSIBLE MANAGED BLOCK`.\n'
                    '\n'
                    'Your task:\n'
                    '> *"Deploy a multi-line security disclaimer into `/etc/issue.net` across all servers in '
                    '`/ansible/block_config.yml`:*\n'
                    '```\n'
                    'Authorized Access Only.\n'
                    'All activities are monitored and logged.\n'
                    '```\n'
                    '*Set `create: true` so the file is created if missing."*',
        'solution_code': '---\n'
                         '- name: Manage Security Banner Block\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Insert banner block in /etc/issue.net\n'
                         '      ansible.builtin.blockinfile:\n'
                         '        path: /etc/issue.net\n'
                         '        create: true\n'
                         '        block: |\n'
                         '          Authorized Access Only.\n'
                         '          All activities are monitored and logged.\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/block_config.yml',
        'tasks': [   '1. Author /ansible/block_config.yml targeting all hosts.',
                     '2. Use ansible.builtin.blockinfile targeting /etc/issue.net.',
                     '3. Insert the 2-line security disclaimer block.',
                     '4. Set create: true so /etc/issue.net is created if absent.',
                     '5. Execute ansible-playbook /ansible/block_config.yml.'],
        'title': 'Lesson 2.5: Managed Multi-Line Blocks — The blockinfile Module',
        'validation_playbook': '---\n'
                               '- name: Validate 2.5\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Read /etc/issue.net\n'
                               '      ansible.builtin.command: cat /etc/issue.net\n'
                               '      register: issue_res\n'
                               '    - name: Assert block contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'Authorized Access Only.\' in issue_res.stdout"\n'
                               '          - "\'All activities are monitored and logged.\' in issue_res.stdout"\n'
                               '          - "\'ANSIBLE MANAGED BLOCK\' in issue_res.stdout"\n',
        'xp': 100},
    {   'difficulty': 'Beginner',
        'explanation': '### Directory Creation in Playbooks\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Scaffold App Directories\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Ensure /opt/dataforge/bin exists\n'
                       '      ansible.builtin.file:\n'
                       '        path: /opt/dataforge/bin\n'
                       '        state: directory\n'
                       "        mode: '0755'\n"
                       '\n'
                       '    - name: Ensure /opt/dataforge/etc exists\n'
                       '      ansible.builtin.file:\n'
                       '        path: /opt/dataforge/etc\n'
                       '        state: directory\n'
                       "        mode: '0755'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/directories.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: file module with state directory',
                         'text': 'tasks:\\n  - name: Create bin\\n    ansible.builtin.file:\\n      path: '
                                 "/opt/dataforge/bin\\n      state: directory\\n      mode: '0755'"}],
        'id': 'l2-6-directory-scaffolding',
        'inspect_cmd': "ansible all -m command -a 'ls -ld /opt/dataforge/bin /opt/dataforge/etc'",
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.file` module with `state: directory` idempotently ensures '
                                 'directories exist. If intermediate parent directories are missing, Ansible creates '
                                 'them automatically.',
                      'demo_code': '---\n'
                                   '- name: Scaffold Directory Structure\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Ensure target directory exists\n'
                                   '      ansible.builtin.file:\n'
                                   '        path: /path/to/directory\n'
                                   '        state: directory\n'
                                   "        mode: '0755'\n",
                      'quick_tip': 'state: directory automatically creates intermediate parent directories if missing.',
                      'syntax_breakdown': [   {   'element': 'state: directory',
                                                  'role': 'Ensures path is a directory (mkdir -p equivalent)'},
                                              {   'element': "mode: '0755'",
                                                  'role': 'Octal permissions string (always quote octal values in '
                                                          'YAML)'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.6\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge /opt/dataforge\n'
                          '      ansible.builtin.file:\n'
                          '        path: /opt/dataforge\n'
                          '        state: absent\n',
        'scenario': 'DataForge is preparing to deploy an in-house telemetry sidecar. The sidecar requires standard '
                    'directories to be present across all hosts:\n'
                    '- `/opt/dataforge/bin`\n'
                    '- `/opt/dataforge/etc`\n'
                    '\n'
                    'In Lesson 1.9, you used `file: state=touch`. In playbooks, `ansible.builtin.file` with `state: '
                    'directory` creates directories and parent directories as needed.\n'
                    '\n'
                    'Author `/ansible/directories.yml` to create both directories with mode `0755` across all nodes.',
        'solution_code': '---\n'
                         '- name: Scaffold App Directories\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Ensure /opt/dataforge/bin exists\n'
                         '      ansible.builtin.file:\n'
                         '        path: /opt/dataforge/bin\n'
                         '        state: directory\n'
                         "        mode: '0755'\n"
                         '\n'
                         '    - name: Ensure /opt/dataforge/etc exists\n'
                         '      ansible.builtin.file:\n'
                         '        path: /opt/dataforge/etc\n'
                         '        state: directory\n'
                         "        mode: '0755'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/directories.yml',
        'tasks': [   '1. Author /ansible/directories.yml targeting all hosts.',
                     '2. Define tasks using ansible.builtin.file with state: directory.',
                     "3. Ensure /opt/dataforge/bin and /opt/dataforge/etc are created with mode '0755'.",
                     '4. Execute ansible-playbook /ansible/directories.yml.'],
        'title': 'Lesson 2.6: Directory Scaffolding — The file Module in Playbooks',
        'validation_playbook': '---\n'
                               '- name: Validate 2.6\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check bin dir\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /opt/dataforge/bin\n'
                               '      register: bin_st\n'
                               '    - name: Check etc dir\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /opt/dataforge/etc\n'
                               '      register: etc_st\n'
                               '    - name: Assert directories exist\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - bin_st.stat.exists and bin_st.stat.isdir\n'
                               '          - etc_st.stat.exists and etc_st.stat.isdir\n',
        'xp': 100},
    {   'difficulty': 'Beginner',
        'explanation': '### The `user` Module\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Provision Service Account\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Ensure deployer user exists\n'
                       '      ansible.builtin.user:\n'
                       '        name: deployer\n'
                       '        shell: /bin/sh\n'
                       '        state: present\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/users.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: user module',
                         'text': 'tasks:\\n  - name: Create deployer user\\n    ansible.builtin.user:\\n      name: '
                                 'deployer\\n      shell: /bin/sh\\n      state: present'}],
        'id': 'l2-7-user-management',
        'inspect_cmd': "ansible all -m command -a 'id deployer'",
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.user` module declaratively creates, updates, or deletes user '
                                 'accounts across diverse Linux operating systems, abstracting `useradd`, `usermod`, '
                                 "`userdel`, and Alpine's `adduser` under one unified interface.",
                      'demo_code': '---\n'
                                   '- name: Provision System User Account\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Ensure user account exists\n'
                                   '      ansible.builtin.user:\n'
                                   '        name: <username>\n'
                                   '        shell: <login_shell_path>\n'
                                   '        state: present\n',
                      'quick_tip': 'On heterogeneous distros (glibc vs Alpine musl), /bin/sh is universally present on '
                                   'all Unix systems.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.user:',
                                                  'role': 'Universal OS user management module'},
                                              {'element': 'name: deployer', 'role': 'Username to manage'},
                                              {'element': 'shell: /bin/sh', 'role': 'Login shell assigned to the user'},
                                              {   'element': 'state: present',
                                                  'role': 'Ensures user exists (idempotent)'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.7\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Delete deployer user\n'
                          '      ansible.builtin.user:\n'
                          '        name: deployer\n'
                          '        state: absent\n'
                          '        remove: true\n',
        'scenario': 'A new junior developer, `deployer`, has joined DataForge. They need an unprivileged service '
                    'account created across all 6 cluster nodes.\n'
                    '\n'
                    'The account must have:\n'
                    '- `name: deployer`\n'
                    '- `shell: /bin/sh` (supported across Alpine and standard glibc distros)\n'
                    '- `state: present`\n'
                    '\n'
                    'Author `/ansible/users.yml` using `ansible.builtin.user` and run it across all nodes.',
        'solution_code': '---\n'
                         '- name: Provision Service Account\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Ensure deployer user exists\n'
                         '      ansible.builtin.user:\n'
                         '        name: deployer\n'
                         '        shell: /bin/sh\n'
                         '        state: present\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/users.yml',
        'tasks': [   '1. Author /ansible/users.yml targeting all hosts.',
                     '2. Use ansible.builtin.user module.',
                     "3. Ensure user 'deployer' is present with shell '/bin/sh'.",
                     '4. Execute ansible-playbook /ansible/users.yml.'],
        'title': 'Lesson 2.7: User Accounts — The user Module',
        'validation_playbook': '---\n'
                               '- name: Validate 2.7\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check deployer user in /etc/passwd\n'
                               '      ansible.builtin.command: id deployer\n'
                               '      register: id_res\n'
                               '      failed_when: id_res.rc != 0\n',
        'xp': 100},
    {   'difficulty': 'Intermediate',
        'explanation': '### Provisioning SSH Keys Declaratively\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Authorize Deployer SSH Key\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Add ed25519 public key\n'
                       '      ansible.builtin.authorized_key:\n'
                       '        user: deployer\n'
                       '        state: present\n'
                       '        key: "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICl1467Hl0GvDataForgeDeployerKey2026 '
                       'deployer@dataforge"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/ssh_keys.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: authorized_key module',
                         'text': 'ansible.builtin.authorized_key:\\n  user: deployer\\n  state: present\\n  key: '
                                 '"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICl1467Hl0GvDataForgeDeployerKey2026 '
                                 'deployer@dataforge"'}],
        'id': 'l2-8-ssh-provisioning',
        'inspect_cmd': "ansible all -m command -a 'cat /home/deployer/.ssh/authorized_keys'",
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.authorized_key` module manages SSH public keys in target user '
                                 'accounts. It automatically creates the `.ssh` directory and `authorized_keys` file '
                                 'with secure permissions (`0700` and `0600`).',
                      'demo_code': '---\n'
                                   '- name: Authorize Public SSH Credentials\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Add public key to authorized_keys\n'
                                   '      ansible.builtin.authorized_key:\n'
                                   '        user: <target_username>\n'
                                   '        state: present\n'
                                   '        key: "<public_key_string>"\n',
                      'quick_tip': 'ansible.builtin.authorized_key creates the ~/.ssh folder and applies strict '
                                   '0700/0600 permissions automatically.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.authorized_key:',
                                                  'role': 'Module managing user authorized_keys entries'},
                                              {   'element': 'user: deployer',
                                                  'role': 'Target username whose ~/.ssh/authorized_keys is updated'},
                                              {'element': 'key: "..."', 'role': 'Public key string or URL'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.8\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove auth key\n'
                          '      ansible.builtin.authorized_key:\n'
                          '        user: deployer\n'
                          '        state: absent\n'
                          '        key: "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICl1467Hl0GvDataForgeDeployerKey2026 '
                          'deployer@dataforge"\n',
        'scenario': 'In Lesson 2.7, you created the `deployer` user. Now, they need passwordless SSH access to run '
                    'CI/CD jobs.\n'
                    '\n'
                    'Security requires provisioning their public key into `~deployer/.ssh/authorized_keys`.\n'
                    '\n'
                    'The public key:\n'
                    '`ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICl1467Hl0GvDataForgeDeployerKey2026 deployer@dataforge`\n'
                    '\n'
                    'Author `/ansible/ssh_keys.yml` using `ansible.builtin.authorized_key`.',
        'solution_code': '---\n'
                         '- name: Authorize Deployer SSH Key\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Add ed25519 public key\n'
                         '      ansible.builtin.authorized_key:\n'
                         '        user: deployer\n'
                         '        state: present\n'
                         '        key: "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICl1467Hl0GvDataForgeDeployerKey2026 '
                         'deployer@dataforge"\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/ssh_keys.yml',
        'tasks': [   '1. Author /ansible/ssh_keys.yml targeting all hosts.',
                     "2. Use ansible.builtin.authorized_key for user 'deployer'.",
                     '3. Set key to the specified ed25519 string.',
                     '4. Run ansible-playbook /ansible/ssh_keys.yml.'],
        'title': 'Lesson 2.8: SSH Key Provisioning — The authorized_key Module',
        'validation_playbook': '---\n'
                               '- name: Validate 2.8\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check authorized_keys exists and contains key\n'
                               '      ansible.builtin.command: grep "DataForgeDeployerKey2026" '
                               '/home/deployer/.ssh/authorized_keys\n'
                               '      register: k_res\n'
                               '      failed_when: k_res.rc != 0\n',
        'xp': 100},
    {   'difficulty': 'Intermediate',
        'explanation': '### Controlling Daemons with `service`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Manage Background Daemons\n'
                       '  hosts: debian\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Ensure cron is active and enabled\n'
                       '      ansible.builtin.service:\n'
                       '        name: cron\n'
                       '        state: started\n'
                       '        enabled: true\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/services.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: service module syntax',
                         'text': 'tasks:\\n  - name: Ensure cron is running\\n    ansible.builtin.service:\\n      '
                                 'name: cron\\n      state: started\\n      enabled: true'}],
        'id': 'l2-9-service-control',
        'inspect_cmd': "ansible debian -m command -a 'service cron status'",
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.service` module controls system services across multiple init '
                                 'systems. It is idempotent: if the daemon is already running, Ansible takes no action '
                                 '(`ok`).',
                      'demo_code': '---\n'
                                   '- name: Control Background System Daemon\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Ensure daemon is running and enabled on boot\n'
                                   '      ansible.builtin.service:\n'
                                   '        name: <service_daemon_name>\n'
                                   '        state: started\n'
                                   '        enabled: true\n',
                      'quick_tip': 'service works across systemd, sysvinit, and openrc without modifying tasks.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.service:',
                                                  'role': 'Module managing system services/daemons'},
                                              {'element': 'name: cron', 'role': 'Name of the service/unit'},
                                              {   'element': 'state: started',
                                                  'role': 'Ensures service process is running '
                                                          '(started/stopped/restarted/reloaded)'},
                                              {   'element': 'enabled: true',
                                                  'role': 'Configures service to start automatically on system boot'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.9\n'
                          '  hosts: debian\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Stop cron for test\n'
                          '      ansible.builtin.service:\n'
                          '        name: cron\n'
                          '        state: stopped\n',
        'scenario': 'Managing files and users is only half the battle; system background daemons must be actively '
                    'running and enabled to survive machine reboots.\n'
                    '\n'
                    'The `ansible.builtin.service` module controls system services (systemd, sysvinit, openrc) in a '
                    'clean, idempotent manner.\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"Target the `debian` server group in `/ansible/services.yml`. Ensure the background daemon '
                    '`cron` is in `state: started` and set `enabled: true` so it starts automatically upon boot."*',
        'solution_code': '---\n'
                         '- name: Manage Background Daemons\n'
                         '  hosts: debian\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Ensure cron is active and enabled\n'
                         '      ansible.builtin.service:\n'
                         '        name: cron\n'
                         '        state: started\n'
                         '        enabled: true\n',
        'solution_type': 'playbook',
        'target': 'debian',
        'target_file': '/ansible/services.yml',
        'tasks': [   '1. Author /ansible/services.yml targeting the debian group.',
                     "2. Use ansible.builtin.service module for service 'cron'.",
                     "3. Ensure state is 'started' and enabled is true.",
                     '4. Execute ansible-playbook /ansible/services.yml.'],
        'title': 'Lesson 2.9: Service Lifecycle — Managing Daemons with service',
        'validation_playbook': '---\n'
                               '- name: Validate 2.9\n'
                               '  hosts: debian\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check cron status\n'
                               '      ansible.builtin.command: service cron status\n'
                               '      register: s_res\n'
                               '      failed_when: s_res.rc != 0\n',
        'xp': 100},
    {   'difficulty': 'Intermediate',
        'explanation': '### Multi-Task Playbook Execution\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Deploy Core Agent Configuration\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Ensure /etc/dataforge directory exists\n'
                       '      ansible.builtin.file:\n'
                       '        path: /etc/dataforge\n'
                       '        state: directory\n'
                       "        mode: '0755'\n"
                       '\n'
                       '    - name: Deploy agent configuration file\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /etc/dataforge/agent.conf\n'
                       '        content: "telemetry_enabled=true\n'
                       'cluster_tier=production\n'
                       '"\n'
                       "        mode: '0644'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/app_config.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Multi-task ordering',
                         'text': 'Place tasks in top-to-bottom order:\\n  tasks:\\n    - name: Create dir\\n      '
                                 'ansible.builtin.file: ...\\n    - name: Create file\\n      ansible.builtin.copy: '
                                 '...'}],
        'id': 'l2-10-multi-task-play',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/dataforge/agent.conf'",
        'module': 'lvl2',
        'primer': {   'concept': 'Ansible plays execute tasks sequentially in exact top-to-bottom order across all '
                                 'targeted hosts. If a prerequisite task fails on a given node, that host is removed '
                                 'from subsequent tasks in the play.',
                      'demo_code': '---\n'
                                   '- name: Sequential Multi-Task Pipeline\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Step 1 - Create parent folder\n'
                                   '      ansible.builtin.file:\n'
                                   '        path: /path/to/folder\n'
                                   '        state: directory\n'
                                   "        mode: '0755'\n"
                                   '\n'
                                   '    - name: Step 2 - Place configuration inside folder\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/folder/config.conf\n'
                                   '        content: "setting_key=value\\n"\n'
                                   "        mode: '0644'\n",
                      'quick_tip': 'Order matters: always place the directory creation task before any task that '
                                   'writes files inside it.',
                      'syntax_breakdown': [   {   'element': 'tasks: [Task 1, Task 2]',
                                                  'role': 'Sequential execution pipeline'},
                                              {   'element': 'Task 1 (file: state=directory)',
                                                  'role': 'Prerequisite directory creation'},
                                              {   'element': 'Task 2 (copy: dest=...)',
                                                  'role': 'File placement inside newly created directory'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.10\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge /etc/dataforge\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/dataforge\n'
                          '        state: absent\n',
        'scenario': 'Real-world playbooks chain multiple dependent tasks together. In Ansible, tasks run sequentially '
                    'in exact top-to-bottom order. If task 1 fails, execution stops immediately!\n'
                    '\n'
                    'Deploy the DataForge core agent directory and configuration in `/ansible/app_config.yml`:\n'
                    '1. Task 1: Ensure directory `/etc/dataforge` exists with mode `0755`.\n'
                    '2. Task 2: Place configuration file `/etc/dataforge/agent.conf` containing '
                    '`telemetry_enabled=true\\ncluster_tier=production\\n` with mode `0644`.',
        'solution_code': '---\n'
                         '- name: Deploy Core Agent Configuration\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Ensure /etc/dataforge directory exists\n'
                         '      ansible.builtin.file:\n'
                         '        path: /etc/dataforge\n'
                         '        state: directory\n'
                         "        mode: '0755'\n"
                         '\n'
                         '    - name: Deploy agent configuration file\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /etc/dataforge/agent.conf\n'
                         '        content: "telemetry_enabled=true\n'
                         'cluster_tier=production\n'
                         '"\n'
                         "        mode: '0644'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/app_config.yml',
        'tasks': [   '1. Author /ansible/app_config.yml targeting all hosts.',
                     "2. Define Task 1 creating directory /etc/dataforge with mode '0755'.",
                     "3. Define Task 2 creating /etc/dataforge/agent.conf with mode '0644'.",
                     '4. Verify task dependency order and run ansible-playbook /ansible/app_config.yml.'],
        'title': 'Lesson 2.10: Orchestration Flow — Multi-Task Plays with Dependencies',
        'validation_playbook': '---\n'
                               '- name: Validate 2.10\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check agent.conf\n'
                               '      ansible.builtin.command: cat /etc/dataforge/agent.conf\n'
                               '      register: ag_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'telemetry_enabled=true\' in ag_res.stdout"\n'
                               '          - "\'cluster_tier=production\' in ag_res.stdout"\n',
        'xp': 100},
    {   'difficulty': 'Intermediate',
        'explanation': '### File Attribute Enforcement\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Harden Agent Security\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Lock down /etc/dataforge/agent.conf permissions\n'
                       '      ansible.builtin.file:\n'
                       '        path: /etc/dataforge/agent.conf\n'
                       '        owner: root\n'
                       '        group: root\n'
                       "        mode: '0600'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/permissions.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Permissions hardening',
                         'text': 'ansible.builtin.file:\\n  path: /etc/dataforge/agent.conf\\n  owner: root\\n  group: '
                                 "root\\n  mode: '0600'"}],
        'id': 'l2-11-permissions-hardening',
        'inspect_cmd': 'ansible all -m command -a \'stat -c "%a %U:%G" /etc/dataforge/agent.conf\'',
        'module': 'lvl2',
        'primer': {   'concept': 'The `ansible.builtin.file` module without `state: directory` or `state: touch` '
                                 'adjusts metadata on existing files (chmod, chown, chgrp). It evaluates current POSIX '
                                 'attributes and only calls `chmod`/`chown` if attributes differ.',
                      'demo_code': '---\n'
                                   '- name: Enforce Strict Security Attributes\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Lock down permissions and ownership\n'
                                   '      ansible.builtin.file:\n'
                                   '        path: /path/to/sensitive_file\n'
                                   '        owner: <user_owner>\n'
                                   '        group: <group_owner>\n'
                                   "        mode: '0600'\n",
                      'quick_tip': "Always quote numeric modes like '0600' in YAML to avoid octal parsing errors.",
                      'syntax_breakdown': [   {'element': 'owner: root', 'role': 'Enforces user ownership'},
                                              {'element': 'group: root', 'role': 'Enforces group ownership'},
                                              {   'element': "mode: '0600'",
                                                  'role': 'Restricts read/write access exclusively to file owner'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.11\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ensure agent.conf exists with loose permissions\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/dataforge/agent.conf\n'
                          "        mode: '0666'\n",
        'scenario': 'During an internal security audit, the compliance officer noticed `/etc/dataforge/agent.conf` has '
                    'loose permissions (readable by anyone).\n'
                    '\n'
                    'DataForge security standards require:\n'
                    '- File owner: `root`\n'
                    '- File group: `root`\n'
                    '- File mode: `0600` (read/write only by root)\n'
                    '\n'
                    'Author `/ansible/permissions.yml` targeting `all` nodes to enforce strict permissions using '
                    '`ansible.builtin.file`.',
        'solution_code': '---\n'
                         '- name: Harden Agent Security\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Lock down /etc/dataforge/agent.conf permissions\n'
                         '      ansible.builtin.file:\n'
                         '        path: /etc/dataforge/agent.conf\n'
                         '        owner: root\n'
                         '        group: root\n'
                         "        mode: '0600'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/permissions.yml',
        'tasks': [   '1. Author /ansible/permissions.yml targeting all hosts.',
                     '2. Use ansible.builtin.file targeting path /etc/dataforge/agent.conf.',
                     "3. Enforce owner: root, group: root, and mode: '0600'.",
                     '4. Run ansible-playbook /ansible/permissions.yml.'],
        'title': 'Lesson 2.11: Security Compliance — Hardening Permissions & Ownership',
        'validation_playbook': '---\n'
                               '- name: Validate 2.11\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check mode of agent.conf\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /etc/dataforge/agent.conf\n'
                               '      register: f_st\n'
                               '    - name: Assert mode is 0600\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               "          - f_st.stat.mode == '0600'\n",
        'xp': 100},
    {   'difficulty': 'Intermediate',
        'explanation': '### Clean Deletions with `state: absent`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Clean Legacy Artifacts\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Purge legacy token\n'
                       '      ansible.builtin.file:\n'
                       '        path: /tmp/legacy_token.key\n'
                       '        state: absent\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/vault.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: state absent',
                         'text': 'ansible.builtin.file:\\n  path: /tmp/legacy_token.key\\n  state: absent'}],
        'id': 'l2-12-purge-deprecated',
        'inspect_cmd': 'ansible all -m command -a \'ls /tmp/legacy_token.key 2>/dev/null || echo "Clean"\'',
        'module': 'lvl2',
        'primer': {   'concept': "The `state: absent` parameter is Ansible's idempotent cleanup mechanism. If the "
                                 'target file or directory exists, Ansible removes it (`changed`). If it is already '
                                 'missing, Ansible succeeds silently (`ok`).',
                      'demo_code': '---\n'
                                   '- name: Clean Obsolete Files\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Purge decommissioned file\n'
                                   '      ansible.builtin.file:\n'
                                   '        path: /path/to/obsolete_file\n'
                                   '        state: absent\n',
                      'quick_tip': "state: absent removes the file if present, or reports 'ok' if already gone.",
                      'syntax_breakdown': [   {   'element': 'path: /tmp/legacy_token.key',
                                                  'role': 'File or folder path to eliminate'},
                                              {   'element': 'state: absent',
                                                  'role': 'Idempotent deletion instruction (rm -rf equivalent)'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.12\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Seed dummy legacy token\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/legacy_token.key\n'
                          '        state: touch\n',
        'scenario': 'A legacy daemon previously wrote temporary plaintext files to `/tmp/legacy_token.key` across all '
                    'servers. Security compliance demands immediate eradication of this file across the fleet.\n'
                    '\n'
                    'In Ansible, setting `state: absent` ensures a file or directory does not exist. If the file is '
                    'already gone, Ansible safely reports `ok`.\n'
                    '\n'
                    'Author `/ansible/vault.yml` targeting `all` nodes to purge `/tmp/legacy_token.key`.',
        'setup_playbook': '---\n'
                          '- name: Setup 2.12\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Seed dummy legacy token\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/legacy_token.key\n'
                          '        state: touch\n',
        'solution_code': '---\n'
                         '- name: Clean Legacy Artifacts\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Purge legacy token\n'
                         '      ansible.builtin.file:\n'
                         '        path: /tmp/legacy_token.key\n'
                         '        state: absent\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/vault.yml',
        'tasks': [   '1. Author /ansible/vault.yml targeting all hosts.',
                     '2. Use ansible.builtin.file with path /tmp/legacy_token.key.',
                     '3. Set state: absent to guarantee file deletion.',
                     '4. Run ansible-playbook /ansible/vault.yml.'],
        'title': 'Lesson 2.12: Asset Hygiene — Purging Deprecated Files with state: absent',
        'validation_playbook': '---\n'
                               '- name: Validate 2.12\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify legacy token is absent\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/legacy_token.key\n'
                               '      register: tok_st\n'
                               '    - name: Assert absent\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - not tok_st.stat.exists\n',
        'xp': 100},
    {   'difficulty': 'Intermediate',
        'explanation': '### Safe Change Management with Check Mode\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Enforce Audit Compliance\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Deploy security audit file\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /etc/security_audit\n'
                       '        content: "compliance_level=gold\n'
                       '"\n'
                       "        mode: '0644'\n"
                       '```\n'
                       'Run simulation:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/compliance.yml --check --diff\n'
                       '```\n'
                       'Apply:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/compliance.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Check mode syntax',
                         'text': 'Run `ansible-playbook /ansible/compliance.yml --check --diff` in the terminal.'}],
        'id': 'l2-13-dry-run-check',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/security_audit'",
        'module': 'lvl2',
        'primer': {   'concept': 'Check mode (`--check`) simulates execution by asking each module whether it would '
                                 'make a change without altering any actual system state. Paired with `--diff`, it '
                                 'provides a crystal-clear preview of upcoming changes.',
                      'demo_code': '---\n'
                                   '- name: Compliance Enforcement\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Ensure compliance file exists\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/audit_file\n'
                                   '        content: "status=verified\\n"\n'
                                   "        mode: '0644'\n",
                      'quick_tip': 'Test execution first in dry-run mode using --check --diff before executing live '
                                   'changes.',
                      'syntax_breakdown': [   {   'element': '--check',
                                                  'role': 'Dry-run flag simulating execution without touching remote '
                                                          'disk'},
                                              {   'element': '--diff',
                                                  'role': 'Displays unified diffs (+/- lines) of proposed file '
                                                          'modifications'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.13\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove audit file\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/security_audit\n'
                          '        state: absent\n',
        'scenario': 'In mission-critical production environments, running an untested playbook directly against '
                    'production can cause outages.\n'
                    '\n'
                    'Ansible provides **Check Mode** (dry-run):\n'
                    '- `--check`: Simulates playbook execution without making any disk or state changes. Modules '
                    'predict whether they would have made changes.\n'
                    '- `--diff`: Displays unified diffs (`+` and `-`) showing exactly what lines would be altered.\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"1. Create `/ansible/compliance.yml` that ensures `/etc/security_audit` contains '
                    '`compliance_level=gold\\n`.*\n'
                    '> *2. Run it in check mode: `ansible-playbook /ansible/compliance.yml --check --diff` to preview '
                    'changes safely.*\n'
                    '> *3. Finally, execute without `--check` to apply the changes."*',
        'solution_code': '---\n'
                         '- name: Enforce Audit Compliance\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Deploy security audit file\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /etc/security_audit\n'
                         '        content: "compliance_level=gold\n'
                         '"\n'
                         "        mode: '0644'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/compliance.yml',
        'tasks': [   "1. Author /ansible/compliance.yml ensuring /etc/security_audit contains 'compliance_level=gold'.",
                     '2. Run with --check --diff to preview changes in dry-run mode.',
                     '3. Execute without --check to apply changes across all nodes.'],
        'title': 'Lesson 2.13: Dry-Run Mode — Testing Playbooks with --check & --diff',
        'validation_playbook': '---\n'
                               '- name: Validate 2.13\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Verify /etc/security_audit exists\n'
                               '      ansible.builtin.command: cat /etc/security_audit\n'
                               '      register: sa_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'compliance_level=gold\' in sa_res.stdout"\n',
        'xp': 100},
    {   'difficulty': 'Intermediate',
        'explanation': '### Onboarding New Systems into Ansible\n'
                       '1. Append host to `/ansible/inventory.ini`:\n'
                       '```ini\n'
                       '[edge]\n'
                       'node7-alpine ansible_host=node7-alpine ansible_python_interpreter=/usr/bin/python3\n'
                       '```\n'
                       '2. Verify connectivity with ad-hoc ping:\n'
                       '```bash\n'
                       'ansible edge -m ping\n'
                       '```\n'
                       '3. Execute onboarding playbook:\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Onboard Edge Client\n'
                       '  hosts: edge\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Install curl utility\n'
                       '      community.general.apk:\n'
                       '        name: curl\n'
                       '        state: present\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/onboard_client.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: inventory.ini entry',
                         'text': 'Add this to /ansible/inventory.ini:\n[edge]\nnode7-alpine ansible_host=node7-alpine ansible_python_interpreter=/usr/bin/python3'},
                     {   'level': 'Hint 2: Playbook syntax',
                         'text': 'hosts: edge\ntasks:\n  - name: Install curl\n    community.general.apk:\n      name: curl\n      state: present'}],
        'id': 'l2-14-host-onboarding',
        'inspect_cmd': 'ansible edge -m ping',
        'module': 'lvl2',
        'primer': {   'concept': 'Ansible is agentless — it can only manage systems that are registered in an **inventory**. '
                                 'When a new server powers on (`node7-alpine`), you must declare it in `/ansible/inventory.ini` '
                                 'under a group before Ansible commands can reach it.\n\n'
                                 'Once enrolled, you test discovery with `ansible <group> -m ping` and run an onboarding '
                                 'playbook to bootstrap packages and configuration.',
                      'sample_files': [   {   'badge': '📄 Inventory Entry',
                                              'desc': 'Required entry to add at the bottom of /ansible/inventory.ini:',
                                              'path': '/ansible/inventory.ini',
                                              'code': '[edge]\nnode7-alpine ansible_host=node7-alpine ansible_python_interpreter=/usr/bin/python3\n'}],
                      'demo_code': '---\n'
                                   '- name: Onboard Edge Client\n'
                                   '  hosts: edge\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Install essential curl utility\n'
                                   '      community.general.apk:\n'
                                   '        name: curl\n'
                                   '        state: present\n',
                      'quick_tip': "Add '[edge]' with 'node7-alpine' to /ansible/inventory.ini first. Then run 'ansible edge -m ping' before running your playbook.",
                      'syntax_breakdown': [   {'element': '[edge]', 'role': 'New group heading defined in inventory.ini'},
                                              {'element': 'ansible_host=node7-alpine', 'role': 'Target client hostname on Docker network'},
                                              {'element': 'ansible_python_interpreter=/usr/bin/python3', 'role': 'Explicit Python binary path for Alpine'},
                                              {'element': 'hosts: edge', 'role': 'Playbook target restricted to the newly onboarded group'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 2.14 Inventory\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove edge from inventory.ini if present\n'
                          '      ansible.builtin.lineinfile:\n'
                          '        path: /ansible/inventory.ini\n'
                          "        regexp: '^(node7-alpine|\\[edge\\])'\n"
                          '        state: absent\n'
                          '- name: Clean curl from node7-alpine\n'
                          '  hosts: node7-alpine\n'
                          '  gather_facts: false\n'
                          '  vars:\n'
                          '    ansible_python_interpreter: /usr/bin/python3\n'
                          '  tasks:\n'
                          '    - name: Purge curl\n'
                          '      community.general.apk:\n'
                          '        name: curl\n'
                          '        state: absent\n'
                          '      ignore_errors: true\n',
        'scenario': 'DataForge has provisioned a brand-new Alpine edge client on the operations network: `node7-alpine`.\n\n'
                    'Although `node7-alpine` is powered on, it is currently **unmanaged** because it is not listed in your inventory.\n\n'
                    'Your assignment:\n'
                    '> *"1. Open `/ansible/inventory.ini` and append a new group `[edge]` containing:*\n'
                    '> *   `node7-alpine ansible_host=node7-alpine ansible_python_interpreter=/usr/bin/python3`*\n'
                    '> *2. Test discovery: `ansible edge -m ping`*\n'
                    '> *3. Author `/ansible/onboard_client.yml` targeting group `edge` to install `curl` using `community.general.apk`.*\n'
                    '> *4. Execute `ansible-playbook /ansible/onboard_client.yml`."*',
        'solution_code': '---\n'
                         '- name: Onboard Edge Client\n'
                         '  hosts: edge\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Install curl utility\n'
                         '      community.general.apk:\n'
                         '        name: curl\n'
                         '        state: present\n',
        'solution_type': 'playbook',
        'target': 'edge',
        'target_file': '/ansible/onboard_client.yml',
        'tasks': [   '1. Enroll node7-alpine under group [edge] in /ansible/inventory.ini.',
                     '2. Verify connectivity with ad-hoc command: ansible edge -m ping.',
                     '3. Author /ansible/onboard_client.yml targeting group edge.',
                     '4. Ensure package curl is installed on the edge client.',
                     '5. Execute ansible-playbook /ansible/onboard_client.yml.'],
        'title': 'Lesson 2.14: Host Onboarding — Enrolling a Client into Inventory & Bootstrapping SSH Trust',
        'validation_playbook': '---\n'
                               '- name: Validate 2.14 Inventory\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check inventory.ini for node7-alpine\n'
                               '      ansible.builtin.command: grep -E "node7-alpine" /ansible/inventory.ini\n'
                               '      register: inv_check\n'
                               '    - name: Assert inventory entry exists\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'node7-alpine\' in inv_check.stdout"\n'
                               '- name: Validate 2.14 Package on Edge\n'
                               '  hosts: node7-alpine\n'
                               '  gather_facts: false\n'
                               '  vars:\n'
                               '    ansible_python_interpreter: /usr/bin/python3\n'
                               '  tasks:\n'
                               '    - name: Verify curl is installed on node7-alpine\n'
                               '      ansible.builtin.command: which curl\n'
                               '      register: curl_check\n'
                               '    - name: Assert curl exists\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'/usr/bin/curl\' in curl_check.stdout or \'curl\' in curl_check.stdout"\n',
        'xp': 150}]

