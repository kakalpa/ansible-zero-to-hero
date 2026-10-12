# Level 4: Production Engineering — Templates, Handlers & Resilience (Lessons 4.1 to 4.13)

LEVEL4_EXERCISES = [   {   'difficulty': 'Intermediate',
        'explanation': '### Handlers and notify\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Event-Driven Service Management\n'
                       '  hosts: debian\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Update configuration trigger\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /etc/dataforge_reload.conf\n'
                       '        content: "reload_required=true\n'
                       '"\n'
                       '      notify: restart cron\n'
                       '\n'
                       '  handlers:\n'
                       '    - name: restart cron\n'
                       '      ansible.builtin.service:\n'
                       '        name: cron\n'
                       '        state: restarted\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/handlers.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Handlers structure',
                         'text': 'tasks:\\n  - name: Update conf\\n    ansible.builtin.copy:\\n      dest: '
                                 '/etc/dataforge_reload.conf\\n      content: "reload_required=true\\n"\\n    notify: '
                                 'restart cron\\nhandlers:\\n  - name: restart cron\\n    '
                                 'ansible.builtin.service:\\n      name: cron\\n      state: restarted'}],
        'id': 'l4-1-handlers-notify',
        'inspect_cmd': "ansible debian -m command -a 'cat /etc/dataforge_reload.conf'",
        'module': 'lvl4',
        'primer': {   'concept': 'Handlers are event-driven tasks that only run when triggered by another task that '
                                 'reported `changed: true`. They de-duplicate: no matter how many tasks notify a '
                                 'handler, it runs exactly once at the end of the play.',
                      'demo_code': '---\n'
                                   '- name: Event-Driven Service Notification\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Modify configuration file\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/config.conf\n'
                                   '        content: "<new_configuration_data>\\n"\n'
                                   '      notify: <exact_handler_name>\n'
                                   '\n'
                                   '  handlers:\n'
                                   '    - name: <exact_handler_name>\n'
                                   '      ansible.builtin.service:\n'
                                   '        name: <service_daemon>\n'
                                   '        state: restarted\n',
                      'quick_tip': "Handlers run only if the calling task reports 'changed: true'. If 10 tasks notify "
                                   'the same handler, it runs once.',
                      'syntax_breakdown': [   {   'element': 'notify: <Handler Name>',
                                                  'role': 'Emits an event if the task reports changed status'},
                                              {   'element': 'handlers:',
                                                  'role': 'Section defining deferred event listeners'},
                                              {   'element': 'name: <Handler Name>',
                                                  'role': 'Must exactly match the name in notify string'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.1\n'
                          '  hosts: debian\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge trigger file\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/dataforge_reload.conf\n'
                          '        state: absent\n',
        'scenario': 'Welcome to **Level 4: Production Engineering**! In production systems, restarting services every '
                    'time a playbook runs causes unnecessary outages.\n'
                    '\n'
                    'Ansible solves this with **Handlers**:\n'
                    '- Tasks trigger handlers using `notify: <Handler Name>`\n'
                    '- Handlers run ONLY IF the calling task reported `changed: true`\n'
                    '- Even if 5 different tasks notify the same handler, it executes only ONCE at the very end of the '
                    'play!\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/handlers.yml` targeting `debian` nodes. Define a task modifying '
                    '`/etc/dataforge_reload.conf` with content `reload_required=true\\n` and `notify: restart cron`. '
                    'Define the handler under `handlers:` to restart the `cron` service."*',
        'solution_code': '---\n'
                         '- name: Event-Driven Service Management\n'
                         '  hosts: debian\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Update configuration trigger\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /etc/dataforge_reload.conf\n'
                         '        content: "reload_required=true\n'
                         '"\n'
                         '      notify: restart cron\n'
                         '\n'
                         '  handlers:\n'
                         '    - name: restart cron\n'
                         '      ansible.builtin.service:\n'
                         '        name: cron\n'
                         '        state: restarted\n',
        'solution_type': 'playbook',
        'target': 'debian',
        'target_file': '/ansible/handlers.yml',
        'tasks': [   '1. Author /ansible/handlers.yml targeting the debian group.',
                     '2. Define a copy task that modifies /etc/dataforge_reload.conf.',
                     '3. Attach notify: restart cron to the copy task.',
                     '4. Define a handler restart cron under handlers: that restarts the cron service.',
                     '5. Execute ansible-playbook /ansible/handlers.yml.'],
        'title': 'Lesson 4.1: Reactive Handlers — Event-Driven Orchestration with notify',
        'validation_playbook': '---\n'
                               '- name: Validate 4.1\n'
                               '  hosts: debian\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check trigger file\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /etc/dataforge_reload.conf\n'
                               '      register: t_st\n'
                               '    - name: Assert exists\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - t_st.stat.exists\n',
        'xp': 200},
    {   'difficulty': 'Intermediate',
        'explanation': '### Flushing Handlers Immediately\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Immediate Handler Execution\n'
                       '  hosts: debian\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Update configuration trigger\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /etc/dataforge_flush.conf\n'
                       '        content: "flushed=true\n'
                       '"\n'
                       '      notify: restart cron\n'
                       '\n'
                       '    - name: Trigger pending handlers right now\n'
                       '      ansible.builtin.meta: flush_handlers\n'
                       '\n'
                       '    - name: Subsequent task running with fresh daemon\n'
                       '      ansible.builtin.command: service cron status\n'
                       '\n'
                       '  handlers:\n'
                       '    - name: restart cron\n'
                       '      ansible.builtin.service:\n'
                       '        name: cron\n'
                       '        state: restarted\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/flush.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: flush_handlers syntax',
                         'text': '- name: Flush handlers\\n  ansible.builtin.meta: flush_handlers'}],
        'id': 'l4-2-flush-handlers',
        'inspect_cmd': "ansible debian -m command -a 'cat /etc/dataforge_flush.conf'",
        'module': 'lvl4',
        'primer': {   'concept': 'The `ansible.builtin.meta: flush_handlers` task forces Ansible to run all queued '
                                 'handlers immediately at that exact position in the playbook, rather than waiting '
                                 'until the end of the play.',
                      'demo_code': '---\n'
                                   '- name: Mid-Play Handler Flushing\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Step 1 - Trigger change\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/file.conf\n'
                                   '        content: "trigger=1\\n"\n'
                                   '      notify: restart_service\n'
                                   '\n'
                                   '    - name: Step 2 - Execute queued handlers right now\n'
                                   '      ansible.builtin.meta: flush_handlers\n'
                                   '\n'
                                   '    - name: Step 3 - Subsequent task relying on restarted daemon\n'
                                   '      ansible.builtin.command: <verification_command>\n'
                                   '\n'
                                   '  handlers:\n'
                                   '    - name: restart_service\n'
                                   '      ansible.builtin.service:\n'
                                   '        name: <service_name>\n'
                                   '        state: restarted\n',
                      'quick_tip': 'ansible.builtin.meta: flush_handlers forces notified handlers to run immediately '
                                   'instead of waiting for the play end.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.meta: flush_handlers',
                                                  'role': 'Flushes and executes queued handlers mid-play'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.2\n'
                          '  hosts: debian\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge trigger file\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/dataforge_flush.conf\n'
                          '        state: absent\n',
        'scenario': 'Handlers normally wait until all tasks in a play finish before running. But what if subsequent '
                    'tasks in the SAME play depend on the service already being restarted?\n'
                    '\n'
                    'Ansible provides the special directive:\n'
                    '```yaml\n'
                    '- name: Flush handlers immediately\n'
                    '  ansible.builtin.meta: flush_handlers\n'
                    '```\n'
                    'This forces all notified handlers to execute right at that moment before continuing to subsequent '
                    'tasks!\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/flush.yml` targeting `debian` nodes. Update `/etc/dataforge_flush.conf` with '
                    'content `flushed=true\\n`, notify `restart cron`, call `ansible.builtin.meta: flush_handlers`, '
                    'and then verify cron is active in a subsequent task."*',
        'solution_code': '---\n'
                         '- name: Immediate Handler Execution\n'
                         '  hosts: debian\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Update configuration trigger\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /etc/dataforge_flush.conf\n'
                         '        content: "flushed=true\n'
                         '"\n'
                         '      notify: restart cron\n'
                         '\n'
                         '    - name: Trigger pending handlers right now\n'
                         '      ansible.builtin.meta: flush_handlers\n'
                         '\n'
                         '    - name: Subsequent task running with fresh daemon\n'
                         '      ansible.builtin.command: service cron status\n'
                         '\n'
                         '  handlers:\n'
                         '    - name: restart cron\n'
                         '      ansible.builtin.service:\n'
                         '        name: cron\n'
                         '        state: restarted\n',
        'solution_type': 'playbook',
        'target': 'debian',
        'target_file': '/ansible/flush.yml',
        'tasks': [   '1. Author /ansible/flush.yml targeting debian hosts.',
                     '2. Define copy task notifying handler restart cron.',
                     '3. Insert task ansible.builtin.meta: flush_handlers.',
                     '4. Define handler restart cron.',
                     '5. Run ansible-playbook /ansible/flush.yml.'],
        'title': 'Lesson 4.2: Execution Ordering — Flushing Handlers with meta: flush_handlers',
        'validation_playbook': '---\n'
                               '- name: Validate 4.2\n'
                               '  hosts: debian\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check trigger file\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /etc/dataforge_flush.conf\n'
                               '      register: f_st\n'
                               '    - name: Assert exists\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - f_st.stat.exists\n',
        'xp': 200},
    {   'difficulty': 'Intermediate',
        'explanation': '### The `template` Module\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Deploy Dynamic Virtual Host\n'
                       '  hosts: all\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Render virtual host template\n'
                       '      ansible.builtin.template:\n'
                       '        src: /ansible/nginx_vhost.j2\n'
                       '        dest: /etc/nginx_vhost.conf\n'
                       "        mode: '0644'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/template.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: template module',
                         'text': 'ansible.builtin.template:\\n  src: /ansible/nginx_vhost.j2\\n  dest: '
                                 "/etc/nginx_vhost.conf\\n  mode: '0644'"}],
        'id': 'l4-3-jinja2-templates',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/nginx_vhost.conf'",
        'module': 'lvl4',
        'primer': {   'concept': 'The `ansible.builtin.template` module processes templates containing Jinja2 '
                                 'expressions (`{{ ... }}`) and control flow (`{% for %}`, `{% if %}`) on the control '
                                 'node, deploying the dynamically generated result to target hosts.',
                      'sample_files': [   {   'badge': '📄 Jinja2 Template',
                                              'desc': 'Template file on control node (.j2) containing Jinja2 syntax and fact references:',
                                              'path': '/ansible/nginx_vhost.j2',
                                              'code': "server {\n    listen 80;\n    server_name {{ ansible_facts['nodename'] }}.dataforge.internal;\n    location / {\n        root /var/www/html;\n        index index.html;\n    }\n}\n"}],
                      'demo_code': '---\n'
                                   '- name: Render Dynamic Jinja2 Template\n'
                                   '  hosts: all\n'
                                   '  gather_facts: true\n'
                                   '  tasks:\n'
                                   '    - name: Generate remote config from template file\n'
                                   '      ansible.builtin.template:\n'
                                   '        src: /ansible/nginx_vhost.j2\n'
                                   '        dest: /etc/nginx_vhost.conf\n'
                                   "        mode: '0644'\n",
                      'quick_tip': 'The src file lives on your control node and is processed through Jinja2 before '
                                   'sending the output to target hosts.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.template:',
                                                  'role': 'Jinja2 template rendering engine'},
                                              {   'element': 'src: /ansible/nginx_vhost.j2',
                                                  'role': 'Template path located on control machine'},
                                              {   'element': 'dest: /etc/nginx_vhost.conf',
                                                  'role': 'Rendered destination file path on target node'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.3\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge vhost file\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/nginx_vhost.conf\n'
                          '        state: absent\n',
        'scenario': 'While `copy` transfers static text, the `ansible.builtin.template` module renders full Jinja2 '
                    'template files (`.j2`) on the control node before sending the generated configuration to target '
                    'servers.\n'
                    '\n'
                    'We have created `/ansible/nginx_vhost.j2` with:\n'
                    '```jinja2\n'
                    '# DataForge VirtualHost for {{ ansible_hostname }}\n'
                    'server {\n'
                    '    listen 80;\n'
                    '    server_name {{ ansible_hostname }}.dataforge.internal;\n'
                    '    root /var/www/{{ ansible_hostname }};\n'
                    '}\n'
                    '```\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/template.yml` targeting `all` nodes with `gather_facts: true`. Use '
                    '`ansible.builtin.template` to render `src: /ansible/nginx_vhost.j2` into `dest: '
                    '/etc/nginx_vhost.conf` with mode `0644`."*',
        'setup_playbook': '---\n'
                          '- name: Seed template\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Write nginx_vhost.j2\n'
                          '      ansible.builtin.copy:\n'
                          '        dest: /ansible/nginx_vhost.j2\n'
                          '        content: |\n'
                          '          # DataForge VirtualHost for {{ ansible_hostname }}\n'
                          '          server {\n'
                          '              listen 80;\n'
                          '              server_name {{ ansible_hostname }}.dataforge.internal;\n'
                          '              root /var/www/{{ ansible_hostname }};\n'
                          '          }\n',
        'solution_code': '---\n'
                         '- name: Deploy Dynamic Virtual Host\n'
                         '  hosts: all\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Render virtual host template\n'
                         '      ansible.builtin.template:\n'
                         '        src: /ansible/nginx_vhost.j2\n'
                         '        dest: /etc/nginx_vhost.conf\n'
                         "        mode: '0644'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/template.yml',
        'tasks': [   '1. Author /ansible/template.yml targeting all hosts with gather_facts: true.',
                     '2. Use ansible.builtin.template with src: /ansible/nginx_vhost.j2.',
                     "3. Set dest: /etc/nginx_vhost.conf and mode: '0644'.",
                     '4. Run ansible-playbook /ansible/template.yml.'],
        'title': 'Lesson 4.3: Dynamic Templating — The template Module & Jinja2 (.j2)',
        'validation_playbook': '---\n'
                               '- name: Validate 4.3\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check vhost file\n'
                               '      ansible.builtin.command: cat /etc/nginx_vhost.conf\n'
                               '      register: v_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'DataForge VirtualHost\' in v_res.stdout"\n'
                               '          - "inventory_hostname in v_res.stdout or \'node\' in v_res.stdout"\n',
        'xp': 200},
    {   'difficulty': 'Intermediate',
        'explanation': '### Transforming Data with Filters\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Transform Data with Jinja2 Filters\n'
                       '  hosts: ubuntu\n'
                       '  gather_facts: false\n'
                       '  vars:\n'
                       '    app_metadata:\n'
                       '      tier: web\n'
                       '      dc: "{{ dc_name | default(\'datacenter-1\') }}"\n'
                       '  tasks:\n'
                       '    - name: Generate structured JSON configuration\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /tmp/app_metadata.json\n'
                       '        content: "{{ app_metadata | to_nice_json }}\n'
                       '"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/filters.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Jinja2 filter syntax',
                         'text': 'vars:\\n  app_metadata:\\n    tier: web\\n    dc: "{{ dc_name | '
                                 'default(\'datacenter-1\') }}"\\ntasks:\\n  - name: Write JSON\\n    '
                                 'ansible.builtin.copy:\\n      dest: /tmp/app_metadata.json\\n      content: "{{ '
                                 'app_metadata | to_nice_json }}\\n"'}],
        'id': 'l4-4-jinja2-filters',
        'inspect_cmd': "ansible ubuntu -m command -a 'cat /tmp/app_metadata.json'",
        'module': 'lvl4',
        'primer': {   'concept': 'Jinja2 filters transform variables before they are rendered. Chaining filters like '
                                 '`| default(...)` and `| to_nice_json` turns complex nested data structures into '
                                 'valid config files effortlessly.',
                      'demo_code': '---\n'
                                   '- name: Transform Data Using Jinja2 Filters\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  vars:\n'
                                   '    custom_data:\n'
                                   '      tier: "app"\n'
                                   '      region: "{{ region_name | default(\'us-east-1\') }}"\n'
                                   '  tasks:\n'
                                   '    - name: Render serialized JSON file\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/metadata.json\n'
                                   '        content: "{{ custom_data | to_nice_json }}\\n"\n',
                      'quick_tip': "Use the pipe symbol (|) to apply Jinja2 filters like default('fallback') and "
                                   'to_nice_json.',
                      'syntax_breakdown': [   {   'element': "| default('...')",
                                                  'role': 'Provides default value if variable is not defined'},
                                              {   'element': '| to_nice_json',
                                                  'role': 'Serializes Python/YAML dictionary to formatted JSON text'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.4\n'
                          '  hosts: ubuntu\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove app_metadata.json\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/app_metadata.json\n'
                          '        state: absent\n',
        'scenario': 'In Lesson 4.3, you substituted simple variables in templates. But production configurations often '
                    'require data transformations: uppercase conversions, fallback defaults, and JSON serialization.\n'
                    '\n'
                    'Jinja2 filters use the pipe operator `|` to transform data inside `{{ ... }}`.\n'
                    'Key filters:\n'
                    "- `{{ env | default('production') }}`: Uses fallback value if variable is undefined.\n"
                    '- `{{ services_dict | to_nice_json }}`: Formats dictionaries as human-readable indented JSON.\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/filters.yml` targeting `ubuntu`. Define a dictionary variable `app_metadata` '
                    'with keys `tier: web` and `dc: \'{{ dc_name | default("datacenter-1") }}\'`. Render '
                    '`/tmp/app_metadata.json` using `{{ app_metadata | to_nice_json }}\\n`."*',
        'solution_code': '---\n'
                         '- name: Transform Data with Jinja2 Filters\n'
                         '  hosts: ubuntu\n'
                         '  gather_facts: false\n'
                         '  vars:\n'
                         '    app_metadata:\n'
                         '      tier: web\n'
                         '      dc: "{{ dc_name | default(\'datacenter-1\') }}"\n'
                         '  tasks:\n'
                         '    - name: Generate structured JSON configuration\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /tmp/app_metadata.json\n'
                         '        content: "{{ app_metadata | to_nice_json }}\n'
                         '"\n',
        'solution_type': 'playbook',
        'target': 'ubuntu',
        'target_file': '/ansible/filters.yml',
        'tasks': [   '1. Author /ansible/filters.yml targeting group ubuntu.',
                     '2. Define app_metadata dictionary utilizing the default filter.',
                     '3. Render /tmp/app_metadata.json using the to_nice_json filter.',
                     '4. Run ansible-playbook /ansible/filters.yml.'],
        'title': 'Lesson 4.4: Template Data Transformations — Jinja2 Filters',
        'validation_playbook': '---\n'
                               '- name: Validate 4.4\n'
                               '  hosts: ubuntu\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check metadata file\n'
                               '      ansible.builtin.command: cat /tmp/app_metadata.json\n'
                               '      register: m_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'datacenter-1\' in m_res.stdout"\n'
                               '          - "\'"tier": "web"\' in m_res.stdout"\n',
        'xp': 200},
    {   'difficulty': 'Intermediate',
        'explanation': '### Magic Variables: `groups` & `hostvars`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Deploy Dynamic Cluster Topology\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Render cluster map\n'
                       '      ansible.builtin.template:\n'
                       '        src: /ansible/cluster_map.j2\n'
                       '        dest: /etc/cluster_map.txt\n'
                       "        mode: '0644'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/inventory_hosts.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: template module with cluster_map.j2',
                         'text': 'ansible.builtin.template:\\n  src: /ansible/cluster_map.j2\\n  dest: '
                                 "/etc/cluster_map.txt\\n  mode: '0644'"}],
        'id': 'l4-5-dynamic-hosts-template',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/cluster_map.txt'",
        'module': 'lvl4',
        'primer': {   'concept': 'The `groups` and `hostvars` magic variables allow Jinja2 templates to inspect other '
                                 'hosts in the inventory. A single template can dynamically generate upstream proxy '
                                 'configs, /etc/hosts maps, or database replica lists.',
                      'sample_files': [   {   'badge': '📄 Jinja2 Loop Template',
                                              'desc': 'Template file iterating over inventory groups and hostvars:',
                                              'path': '/ansible/cluster_map.j2',
                                              'code': "# DataForge Dynamic Cluster Topology\n{% for host in groups['all'] %}\n{{ host }} - {{ hostvars[host]['ansible_host'] | default(host) }}\n{% endfor %}\n"}],
                      'demo_code': '---\n'
                                   '- name: Deploy Dynamic Cluster Mesh\n'
                                   '  hosts: all\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Render dynamic inventory topology\n'
                                   '      ansible.builtin.template:\n'
                                   '        src: /ansible/cluster_map.j2\n'
                                   '        dest: /etc/cluster_map.txt\n'
                                   "        mode: '0644'\n",
                      'quick_tip': "Inside Jinja2 templates (.j2), use {% for host in groups['all'] %} to iterate "
                                   'through all inventory hosts dynamically.',
                      'syntax_breakdown': [   {   'element': "groups['all']",
                                                   'role': 'Magic variable containing list of all inventory hostnames'},
                                              {   'element': 'hostvars[host]',
                                                  'role': 'Magic dictionary containing facts and variables of another '
                                                          'host'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.5\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge cluster map\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/cluster_map.txt\n'
                          '        state: absent\n',
        'scenario': 'In complex distributed environments, cluster nodes need to know about all other nodes in the '
                    'cluster (e.g. for consensus, load balancing, or mesh networking).\n'
                    '\n'
                    'Ansible exposes the magic variable `groups`:\n'
                    "- `groups['all']`: List of all hosts in the inventory\n"
                    "- `groups['debian']`: List of all Debian hosts\n"
                    '\n'
                    'We have created `/ansible/cluster_map.j2`:\n'
                    '```jinja2\n'
                    '# DataForge Dynamic Cluster Topology\n'
                    "{% for host in groups['all'] %}\n"
                    "{{ host }} - {{ hostvars[host]['ansible_host'] | default(host) }}\n"
                    '{% endfor %}\n'
                    '```\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/inventory_hosts.yml` targeting `all` nodes. Render `src: '
                    '/ansible/cluster_map.j2` into `dest: /etc/cluster_map.txt` with mode `0644`."*',
        'setup_playbook': '---\n'
                          '- name: Seed cluster_map.j2\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Write cluster_map.j2\n'
                          '      ansible.builtin.copy:\n'
                          '        dest: /ansible/cluster_map.j2\n'
                          '        content: |\n'
                          '          # DataForge Dynamic Cluster Topology\n'
                          "          {% for host in groups['all'] %}\n"
                          "          {{ host }} - {{ hostvars[host]['ansible_host'] | default(host) }}\n"
                          '          {% endfor %}\n',
        'solution_code': '---\n'
                         '- name: Deploy Dynamic Cluster Topology\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Render cluster map\n'
                         '      ansible.builtin.template:\n'
                         '        src: /ansible/cluster_map.j2\n'
                         '        dest: /etc/cluster_map.txt\n'
                         "        mode: '0644'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/inventory_hosts.yml',
        'tasks': [   '1. Author /ansible/inventory_hosts.yml targeting all hosts.',
                     '2. Use template module with src: /ansible/cluster_map.j2.',
                     '3. Set dest: /etc/cluster_map.txt.',
                     '4. Run ansible-playbook /ansible/inventory_hosts.yml.'],
        'title': 'Lesson 4.5: Dynamic Cluster Map — Templating Inventory Slices with groups',
        'validation_playbook': '---\n'
                               '- name: Validate 4.5\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check map\n'
                               '      ansible.builtin.command: cat /etc/cluster_map.txt\n'
                               '      register: m_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'DataForge Dynamic Cluster Topology\' in m_res.stdout"\n'
                               '          - "\'node1-ubuntu\' in m_res.stdout"\n'
                               '          - "\'node6-alpine\' in m_res.stdout"\n',
        'xp': 200},
    {   'difficulty': 'Intermediate',
        'explanation': '### Modular Playbooks with `import_tasks`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Master Infrastructure Orchestration\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Execute common baseline tasks\n'
                       '      ansible.builtin.import_tasks: /ansible/tasks_common.yml\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/site.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: import_tasks syntax',
                         'text': 'tasks:\\n  - name: Import common tasks\\n    ansible.builtin.import_tasks: '
                                 '/ansible/tasks_common.yml'}],
        'id': 'l4-6-modular-tasks',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/modular_tag.txt'",
        'module': 'lvl4',
        'primer': {   'concept': 'The `ansible.builtin.import_tasks` directive statically imports an external YAML '
                                 'list of tasks at playbook parse time. This promotes modular code organization and '
                                 'reuse across multiple plays.',
                      'demo_code': '---\n'
                                   '- name: Modular Playbook Architecture\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Include external task list\n'
                                   '      ansible.builtin.import_tasks: /path/to/modular_tasks.yml\n',
                      'quick_tip': 'import_tasks statically incorporates task files at parse time, keeping master '
                                   'playbooks clean and readable.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.import_tasks:',
                                                  'role': 'Static task inclusion at parse time'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.6\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge modular tag\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/modular_tag.txt\n'
                          '        state: absent\n',
        'scenario': 'Monolithic 500-line playbooks become unmaintainable. Professional teams split playbooks into '
                    'modular task files and include them via `ansible.builtin.import_tasks`.\n'
                    '\n'
                    'We have created modular task file `/ansible/tasks_common.yml`:\n'
                    '```yaml\n'
                    '- name: Set modular node tag\n'
                    '  ansible.builtin.copy:\n'
                    '    dest: /etc/modular_tag.txt\n'
                    '    content: "modular_build=active\n'
                    '"\n'
                    '```\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create master playbook `/ansible/site.yml` targeting `all` nodes. Use '
                    '`ansible.builtin.import_tasks: /ansible/tasks_common.yml` to execute the modular tasks."*',
        'setup_playbook': '---\n'
                          '- name: Seed tasks_common.yml\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Write tasks_common.yml\n'
                          '      ansible.builtin.copy:\n'
                          '        dest: /ansible/tasks_common.yml\n'
                          '        content: |\n'
                          '          - name: Set modular node tag\n'
                          '            ansible.builtin.copy:\n'
                          '              dest: /etc/modular_tag.txt\n'
                          '              content: "modular_build=active\n'
                          '"\n',
        'solution_code': '---\n'
                         '- name: Master Infrastructure Orchestration\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Execute common baseline tasks\n'
                         '      ansible.builtin.import_tasks: /ansible/tasks_common.yml\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/site.yml',
        'tasks': [   '1. Author /ansible/site.yml targeting all hosts.',
                     '2. Use ansible.builtin.import_tasks to include /ansible/tasks_common.yml.',
                     '3. Run ansible-playbook /ansible/site.yml.'],
        'title': 'Lesson 4.6: Modular Decomposition — Reusing Tasks with import_tasks',
        'validation_playbook': '---\n'
                               '- name: Validate 4.6\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check modular tag\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /etc/modular_tag.txt\n'
                               '      register: m_st\n'
                               '    - name: Assert exists\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - m_st.stat.exists\n',
        'xp': 200},
    {   'difficulty': 'Intermediate',
        'explanation': '### Selective Execution with Tags\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Selective Execution with Tags\n'
                       '  hosts: debian\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Apply fast configuration change\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /tmp/tagged_config.conf\n'
                       '        content: "feature_flags=v2\n'
                       '"\n'
                       '      tags:\n'
                       '        - config\n'
                       '\n'
                       '    - name: Long running database migration\n'
                       '      ansible.builtin.command: sleep 1\n'
                       '      tags:\n'
                       '        - slow_maintenance\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/tagged_tasks.yml --tags config\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Tags syntax',
                         'text': 'tasks:\\n  - name: Apply config\\n    ansible.builtin.copy:\\n      dest: '
                                 '/tmp/tagged_config.conf\\n      content: "feature_flags=v2\\n"\\n    tags:\\n      - '
                                 'config'}],
        'id': 'l4-7-tags-execution',
        'inspect_cmd': "ansible debian -m command -a 'cat /tmp/tagged_config.conf'",
        'module': 'lvl4',
        'primer': {   'concept': 'Tags categorize tasks within playbooks. Running `ansible-playbook --tags <tag>` '
                                 'executes only the matched tasks, skipping everything else. Conversely, `--skip-tags '
                                 '<tag>` excludes specific tasks.',
                      'demo_code': '---\n'
                                   '- name: Selective Orchestration with Tags\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Fast configuration task\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/config.conf\n'
                                   '        content: "flag=true\\n"\n'
                                   '      tags:\n'
                                   '        - <tag_name>\n'
                                   '\n'
                                   '    - name: Long running task\n'
                                   '      ansible.builtin.command: sleep 5\n'
                                   '      tags:\n'
                                   '        - maintenance\n',
                      'quick_tip': 'Execute only tagged tasks from the CLI using: ansible-playbook <playbook.yml> '
                                   '--tags <tag_name>.',
                      'syntax_breakdown': [   {   'element': 'tags: [config]',
                                                  'role': 'Labels task with one or more tag strings'},
                                              {   'element': '--tags <name>',
                                                  'role': 'CLI argument restricting execution to matching tags'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.7\n'
                          '  hosts: debian\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge tagged config\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/tagged_config.conf\n'
                          '        state: absent\n',
        'scenario': 'In large playbooks, executing every task on every run is too slow. Ansible **Tags** allow '
                    'labeling tasks so you can selectively run or skip parts of a playbook.\n'
                    '\n'
                    'The command `ansible-playbook --tags <tag_name>` runs only tagged tasks!\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/tagged_tasks.yml` targeting `debian` nodes. Define two tasks:*\n'
                    '> *1. Task 1: deploy `/tmp/tagged_config.conf` with content `feature_flags=v2\\n`, labeled with '
                    '`tags: [config]`.*\n'
                    '> *2. Task 2: run `sleep 1`, labeled with `tags: [slow_maintenance]`.*\n'
                    '> *Execute the playbook selectively using: `ansible-playbook /ansible/tagged_tasks.yml --tags '
                    'config`."*',
        'solution_code': '---\n'
                         '- name: Selective Execution with Tags\n'
                         '  hosts: debian\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Apply fast configuration change\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /tmp/tagged_config.conf\n'
                         '        content: "feature_flags=v2\n'
                         '"\n'
                         '      tags:\n'
                         '        - config\n'
                         '\n'
                         '    - name: Long running database migration\n'
                         '      ansible.builtin.command: sleep 1\n'
                         '      tags:\n'
                         '        - slow_maintenance\n',
        'solution_type': 'playbook',
        'target': 'debian',
        'target_file': '/ansible/tagged_tasks.yml',
        'tasks': [   '1. Author /ansible/tagged_tasks.yml targeting debian hosts.',
                     '2. Label Task 1 with tags: [config].',
                     '3. Label Task 2 with tags: [slow_maintenance].',
                     '4. Run ansible-playbook /ansible/tagged_tasks.yml --tags config.'],
        'title': 'Lesson 4.7: Selective Execution — Orchestration with Tags',
        'validation_playbook': '---\n'
                               '- name: Validate 4.7\n'
                               '  hosts: debian\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check tagged config\n'
                               '      ansible.builtin.command: cat /tmp/tagged_config.conf\n'
                               '      register: c_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'feature_flags=v2\' in c_res.stdout"\n',
        'xp': 200},
    {   'difficulty': 'Advanced',
        'explanation': '### Scaffolding Roles with `ansible-galaxy`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Scaffold Enterprise Role\n'
                       '  hosts: localhost\n'
                       '  connection: local\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Ensure roles directory exists\n'
                       '      ansible.builtin.file:\n'
                       '        path: /ansible/roles\n'
                       '        state: directory\n'
                       '\n'
                       '    - name: Initialize webserver role\n'
                       '      ansible.builtin.command: ansible-galaxy role init /ansible/roles/webserver\n'
                       '      args:\n'
                       '        creates: /ansible/roles/webserver/tasks/main.yml\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/roles_scaffold.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Scaffolding a role',
                         'text': 'tasks:\\n  - name: Ensure roles dir\\n    ansible.builtin.file:\\n      path: '
                                 '/ansible/roles\\n      state: directory\\n  - name: Init role\\n    '
                                 'ansible.builtin.command: ansible-galaxy role init /ansible/roles/webserver\\n    '
                                 'args:\\n      creates: /ansible/roles/webserver/tasks/main.yml'}],
        'id': 'l4-8-role-scaffolding',
        'inspect_cmd': 'ls -ld /ansible/roles/webserver/tasks',
        'module': 'lvl4',
        'primer': {   'concept': 'Roles package automation into self-contained, distributable units. `ansible-galaxy '
                                 'role init <name>` creates standard directories (`tasks/`, `handlers/`, `defaults/`, '
                                 '`vars/`, `templates/`), making collaboration intuitive across large engineering '
                                 'teams.',
                      'demo_code': '---\n'
                                   '- name: Scaffold Standard Role Architecture\n'
                                   '  hosts: localhost\n'
                                   '  connection: local\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Create role directory tree using ansible-galaxy\n'
                                   '      ansible.builtin.command: ansible-galaxy role init '
                                   '/path/to/roles/<role_name>\n'
                                   '      args:\n'
                                   '        creates: /path/to/roles/<role_name>/tasks/main.yml\n',
                      'quick_tip': 'ansible-galaxy role init generates standard directories: tasks/, handlers/, '
                                   'templates/, vars/, and defaults/.',
                      'syntax_breakdown': [   {   'element': 'ansible-galaxy role init ...',
                                                  'role': 'CLI scaffolding tool generating standard role directories'},
                                              {   'element': 'creates: ...',
                                                  'role': 'Prevents command from re-running if directory already '
                                                          'exists'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.8\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge role directory\n'
                          '      ansible.builtin.file:\n'
                          '        path: /ansible/roles/webserver\n'
                          '        state: absent\n',
        'scenario': 'In enterprise Ansible codebases, `import_tasks` is superseded by **Roles**. Roles provide a '
                    'standard directory layout separating tasks, handlers, variables, defaults, templates, and files.\n'
                    '\n'
                    'Standard role directory layout:\n'
                    '- `tasks/main.yml`\n'
                    '- `handlers/main.yml`\n'
                    '- `defaults/main.yml`\n'
                    '- `vars/main.yml`\n'
                    '- `templates/`\n'
                    '\n'
                    'The `ansible-galaxy role init <name>` command scaffolds this structure automatically!\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/roles_scaffold.yml` running on `localhost`. Use `ansible.builtin.command` to '
                    'initialize the role `webserver` inside directory `/ansible/roles` (`ansible-galaxy role init '
                    '/ansible/roles/webserver`)."*',
        'solution_code': '---\n'
                         '- name: Scaffold Enterprise Role\n'
                         '  hosts: localhost\n'
                         '  connection: local\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Ensure roles directory exists\n'
                         '      ansible.builtin.file:\n'
                         '        path: /ansible/roles\n'
                         '        state: directory\n'
                         '\n'
                         '    - name: Initialize webserver role\n'
                         '      ansible.builtin.command: ansible-galaxy role init /ansible/roles/webserver\n'
                         '      args:\n'
                         '        creates: /ansible/roles/webserver/tasks/main.yml\n',
        'solution_type': 'playbook',
        'target': 'localhost',
        'target_file': '/ansible/roles_scaffold.yml',
        'tasks': [   '1. Author /ansible/roles_scaffold.yml targeting localhost with connection: local.',
                     '2. Ensure directory /ansible/roles exists.',
                     '3. Run ansible-galaxy role init /ansible/roles/webserver.',
                     '4. Execute ansible-playbook /ansible/roles_scaffold.yml.'],
        'title': 'Lesson 4.8: Production Architecture — Scaffolding Ansible Roles with ansible-galaxy',
        'validation_playbook': '---\n'
                               '- name: Validate 4.8\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check tasks/main.yml\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /ansible/roles/webserver/tasks/main.yml\n'
                               '      register: r_st\n'
                               '    - name: Assert role initialized\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - r_st.stat.exists\n',
        'xp': 200},
    {   'difficulty': 'Advanced',
        'explanation': '### Applying Roles in Playbooks\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Apply Enterprise Roles\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  roles:\n'
                       '    - role: /ansible/roles/webserver\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/roles_site.yml\n'
                       '```',
        'hints': [{'level': 'Hint 1: roles section', 'text': 'roles:\\n  - role: /ansible/roles/webserver'}],
        'id': 'l4-9-role-execution',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/webserver_role.status'",
        'module': 'lvl4',
        'primer': {   'concept': 'The `roles:` section applies modular roles to target hosts. Ansible automatically '
                                 "executes the role's `tasks/main.yml`, loads `defaults/main.yml`, and registers its "
                                 '`handlers/main.yml`.',
                      'demo_code': '---\n'
                                   '- name: Execute Enterprise Roles\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  roles:\n'
                                   '    - role: /path/to/roles/<role_name>\n',
                      'quick_tip': 'When a role is specified under roles:, Ansible automatically executes its '
                                   'tasks/main.yml and loads all role assets.',
                      'syntax_breakdown': [   {   'element': 'roles:',
                                                  'role': 'Top-level play section defining roles applied to hosts'},
                                              {   'element': '- role: /path',
                                                  'role': 'Path or name of the role to execute'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.9\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge role status file\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/webserver_role.status\n'
                          '        state: absent\n',
        'scenario': "In Lesson 4.8, you scaffolded the `webserver` role. Now let's populate it and execute it across "
                    'all nodes!\n'
                    '\n'
                    'We have populated `/ansible/roles/webserver/tasks/main.yml` with:\n'
                    '```yaml\n'
                    '- name: Deploy webserver role signature\n'
                    '  ansible.builtin.copy:\n'
                    '    dest: /etc/webserver_role.status\n'
                    '    content: "role=webserver\n'
                    'version=1.0.0\n'
                    '"\n'
                    "    mode: '0644'\n"
                    '```\n'
                    '\n'
                    'In Ansible, a play invokes roles using the `roles:` directive:\n'
                    '```yaml\n'
                    '- name: Apply Webserver Role\n'
                    '  hosts: all\n'
                    '  roles:\n'
                    '    - role: /ansible/roles/webserver\n'
                    '```\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/roles_site.yml` targeting `all` nodes and invoke the role '
                    '`/ansible/roles/webserver`."*',
        'setup_playbook': '---\n'
                          '- name: Seed webserver role tasks\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ensure tasks dir\n'
                          '      ansible.builtin.file:\n'
                          '        path: /ansible/roles/webserver/tasks\n'
                          '        state: directory\n'
                          '    - name: Write tasks/main.yml\n'
                          '      ansible.builtin.copy:\n'
                          '        dest: /ansible/roles/webserver/tasks/main.yml\n'
                          '        content: |\n'
                          '          - name: Deploy webserver role signature\n'
                          '            ansible.builtin.copy:\n'
                          '              dest: /etc/webserver_role.status\n'
                          '              content: "role=webserver\n'
                          'version=1.0.0\n'
                          '"\n'
                          "              mode: '0644'\n",
        'solution_code': '---\n'
                         '- name: Apply Enterprise Roles\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  roles:\n'
                         '    - role: /ansible/roles/webserver\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/roles_site.yml',
        'tasks': [   '1. Author /ansible/roles_site.yml targeting all hosts.',
                     '2. Use the roles: directive to invoke /ansible/roles/webserver.',
                     '3. Execute ansible-playbook /ansible/roles_site.yml across all 6 cluster nodes.'],
        'title': 'Lesson 4.9: Role Execution — Applying Reusable Roles across Fleet',
        'validation_playbook': '---\n'
                               '- name: Validate 4.9\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check role status\n'
                               '      ansible.builtin.command: cat /etc/webserver_role.status\n'
                               '      register: s_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'role=webserver\' in s_res.stdout"\n',
        'xp': 200},
    {   'difficulty': 'Advanced',
        'explanation': '### Secrets Hygiene with Ansible Vault\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Deploy Encrypted Secret\n'
                       '  hosts: ubuntu\n'
                       '  gather_facts: false\n'
                       '  vars_files:\n'
                       '    - /ansible/secrets.yml\n'
                       '  tasks:\n'
                       '    - name: Write secure token\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /tmp/vault_applied.token\n'
                       '        content: "API_KEY={{ api_secret_token }}\n'
                       '"\n'
                       "        mode: '0600'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/vault_secret.yml --vault-password-file /ansible/.vault_pass\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Vault playbook',
                         'text': 'vars_files:\\n  - /ansible/secrets.yml\\ntasks:\\n  - name: Write secret\\n    '
                                 'ansible.builtin.copy:\\n      dest: /tmp/vault_applied.token\\n      content: '
                                 '"API_KEY={{ api_secret_token }}\\n"\\n      mode: \'0600\''}],
        'id': 'l4-10-ansible-vault',
        'inspect_cmd': "ansible ubuntu -m command -a 'cat /tmp/vault_applied.token'",
        'module': 'lvl4',
        'primer': {   'concept': 'Ansible Vault protects sensitive credentials by encrypting YAML files with AES-256. '
                                 'Decryption occurs transparently in memory when the playbook runs with '
                                 '`--vault-password-file` or `--ask-vault-pass`.',
                      'demo_code': '---\n'
                                   '- name: Deploy Encrypted Vault Secrets\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  vars_files:\n'
                                   '    - /path/to/encrypted_vault_file.yml\n'
                                   '  tasks:\n'
                                   '    - name: Deploy secret credential securely\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/secret.token\n'
                                   '        content: "SECRET_KEY={{ vaulted_variable_name }}\\n"\n'
                                   "        mode: '0600'\n",
                      'quick_tip': 'Execute playbooks containing vaulted files using: ansible-playbook <playbook.yml> '
                                   '--vault-password-file <keyfile>.',
                      'syntax_breakdown': [   {   'element': '--vault-password-file',
                                                  'role': 'Path to file containing vault decryption key'},
                                              {   'element': 'vars_files: [ secrets.yml ]',
                                                  'role': 'Loads encrypted YAML file seamlessly'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.10\n'
                          '  hosts: ubuntu\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove vault_applied.token\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/vault_applied.token\n'
                          '        state: absent\n',
        'scenario': 'Production playbooks must never store plain-text database passwords, tokens, or private keys in '
                    'git repositories.\n'
                    '\n'
                    '`ansible-vault` encrypts variables and YAML files using AES-256. At execution time, '
                    '`--vault-password-file` passes the password to decrypt the secrets in memory without writing '
                    'plaintext to disk.\n'
                    '\n'
                    'We have provisioned an encrypted secret file at `/ansible/secrets.yml` and the password file at '
                    '`/ansible/.vault_pass`. Inside `secrets.yml`, variable `api_secret_token` is stored.\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/vault_secret.yml` targeting `ubuntu`. Load `/ansible/secrets.yml` using '
                    '`vars_files:` and write `/tmp/vault_applied.token` with content `API_KEY={{ api_secret_token '
                    '}}\\n` and mode `0600`.*\n'
                    '> *Execute with: `ansible-playbook /ansible/vault_secret.yml --vault-password-file '
                    '/ansible/.vault_pass`."*',
        'setup_playbook': '---\n'
                          '- name: Setup encrypted secrets\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Write vault pass\n'
                          '      ansible.builtin.copy:\n'
                          '        dest: /ansible/.vault_pass\n'
                          '        content: "DataForgeMasterKey2026\n'
                          '"\n'
                          "        mode: '0600'\n"
                          '    - name: Write plaintext secret temporarily\n'
                          '      ansible.builtin.copy:\n'
                          '        dest: /tmp/plain_secrets.yml\n'
                          '        content: "api_secret_token: \'df-sec-99214-alpha\'\n'
                          '"\n'
                          '    - name: Encrypt secrets.yml\n'
                          '      ansible.builtin.command: ansible-vault encrypt /tmp/plain_secrets.yml '
                          '--vault-password-file /ansible/.vault_pass --output /ansible/secrets.yml\n',
        'solution_code': '---\n'
                         '- name: Deploy Encrypted Secret\n'
                         '  hosts: ubuntu\n'
                         '  gather_facts: false\n'
                         '  vars_files:\n'
                         '    - /ansible/secrets.yml\n'
                         '  tasks:\n'
                         '    - name: Write secure token\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /tmp/vault_applied.token\n'
                         '        content: "API_KEY={{ api_secret_token }}\n'
                         '"\n'
                         "        mode: '0600'\n",
        'solution_type': 'playbook',
        'target': 'ubuntu',
        'target_file': '/ansible/vault_secret.yml',
        'tasks': [   '1. Author /ansible/vault_secret.yml targeting ubuntu.',
                     '2. Load encrypted secrets using vars_files: [ /ansible/secrets.yml ].',
                     "3. Write /tmp/vault_applied.token with mode '0600' containing {{ api_secret_token }}.",
                     '4. Execute with --vault-password-file /ansible/.vault_pass.'],
        'title': 'Lesson 4.10: Secrets Hygiene — Encrypted Variables with ansible-vault',
        'validation_playbook': '---\n'
                               '- name: Validate 4.10\n'
                               '  hosts: ubuntu\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check token\n'
                               '      ansible.builtin.command: cat /tmp/vault_applied.token\n'
                               '      register: t_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'API_KEY=df-sec-99214-alpha\' in t_res.stdout"\n',
        'xp': 200},
    {   'difficulty': 'Advanced',
        'explanation': '### Resilience with `block / rescue / always`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Resilient Operations\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Transactional operation\n'
                       '      block:\n'
                       '        - name: Primary operation that might fail\n'
                       '          ansible.builtin.command: /bin/false\n'
                       '\n'
                       '      rescue:\n'
                       '        - name: Emergency rollback or remediation\n'
                       '          ansible.builtin.copy:\n'
                       '            dest: /tmp/rescue_activated.log\n'
                       '            content: "Recovery Executed\n'
                       '"\n'
                       '\n'
                       '      always:\n'
                       '        - name: Guaranteed cleanup\n'
                       '          ansible.builtin.copy:\n'
                       '            dest: /tmp/always_cleanup.log\n'
                       '            content: "Cleanup Done\n'
                       '"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/rescue.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: block rescue syntax',
                         'text': 'tasks:\\n  - name: Resilient block\\n    block:\\n      - ansible.builtin.command: '
                                 '/bin/false\\n    rescue:\\n      - ansible.builtin.copy:\\n          dest: '
                                 '/tmp/rescue_activated.log\\n          content: "Recovery Executed\\n"\\n    '
                                 'always:\\n      - ansible.builtin.copy:\\n          dest: '
                                 '/tmp/always_cleanup.log\\n          content: "Cleanup Done\\n"'}],
        'id': 'l4-11-fault-tolerance',
        'inspect_cmd': "ansible all -m command -a 'cat /tmp/rescue_activated.log /tmp/always_cleanup.log'",
        'module': 'lvl4',
        'primer': {   'concept': 'The `block`, `rescue`, and `always` structure functions like `try / catch / finally` '
                                 'in modern programming languages, giving playbooks transactional rollback and '
                                 'guaranteed cleanup capabilities.',
                      'demo_code': '---\n'
                                   '- name: Transactional Resilience Workflow\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Protected transactional block\n'
                                   '      block:\n'
                                   '        - name: Primary operation that may fail\n'
                                   '          ansible.builtin.command: <risky_command>\n'
                                   '\n'
                                   '      rescue:\n'
                                   '        - name: Fallback remediation on error\n'
                                   '          ansible.builtin.copy:\n'
                                   '            dest: /var/log/rollback.log\n'
                                   '            content: "Failure caught and handled\\n"\n'
                                   '\n'
                                   '      always:\n'
                                   '        - name: Guaranteed cleanup task\n'
                                   '          ansible.builtin.copy:\n'
                                   '            dest: /var/log/cleanup.log\n'
                                   '            content: "Execution complete\\n"\n',
                      'quick_tip': 'block / rescue / always behaves like try / catch / finally: rescue only runs if '
                                   'block fails; always runs unconditionally.',
                      'syntax_breakdown': [   {   'element': 'block:',
                                                  'role': 'Group of primary tasks executed in sequence'},
                                              {   'element': 'rescue:',
                                                  'role': 'Recovery tasks executed only if a task in block fails'},
                                              {   'element': 'always:',
                                                  'role': 'Guaranteed tasks executed regardless of success or '
                                                          'failure'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.11\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge logs\n'
                          '      ansible.builtin.file:\n'
                          '        path: "{{ item }}"\n'
                          '        state: absent\n'
                          '      loop:\n'
                          '        - /tmp/rescue_activated.log\n'
                          '        - /tmp/always_cleanup.log\n',
        'scenario': 'In distributed systems, tasks occasionally fail (network hiccups, transient disk errors, '
                    'timeouts). Unhandled failures abort execution.\n'
                    '\n'
                    'Ansible provides structured exception handling using `block`, `rescue`, and `always`:\n'
                    '- `block`: Main task execution\n'
                    '- `rescue`: Executes ONLY if any task inside `block` fails (error recovery / rollback)\n'
                    '- `always`: Executes regardless of success or failure (cleanup locks, remove tmp files)\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/rescue.yml` targeting `all` nodes:*\n'
                    '> *1. Inside `block`, attempt running a failing command: `ansible.builtin.command: /bin/false`.*\n'
                    '> *2. Inside `rescue`, catch the failure and write `/tmp/rescue_activated.log` with content '
                    '`Recovery Executed\\n`.*\n'
                    '> *3. Inside `always`, place `/tmp/always_cleanup.log` with content `Cleanup Done\\n`."*',
        'solution_code': '---\n'
                         '- name: Resilient Operations\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Transactional operation\n'
                         '      block:\n'
                         '        - name: Primary operation that might fail\n'
                         '          ansible.builtin.command: /bin/false\n'
                         '\n'
                         '      rescue:\n'
                         '        - name: Emergency rollback or remediation\n'
                         '          ansible.builtin.copy:\n'
                         '            dest: /tmp/rescue_activated.log\n'
                         '            content: "Recovery Executed\n'
                         '"\n'
                         '\n'
                         '      always:\n'
                         '        - name: Guaranteed cleanup\n'
                         '          ansible.builtin.copy:\n'
                         '            dest: /tmp/always_cleanup.log\n'
                         '            content: "Cleanup Done\n'
                         '"\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/rescue.yml',
        'tasks': [   '1. Author /ansible/rescue.yml targeting all hosts.',
                     '2. Define block containing failing command /bin/false.',
                     '3. Define rescue containing copy task writing /tmp/rescue_activated.log.',
                     '4. Define always containing copy task writing /tmp/always_cleanup.log.',
                     '5. Execute ansible-playbook /ansible/rescue.yml.'],
        'title': 'Lesson 4.11: Fault Tolerance & Resilience — block / rescue / always',
        'validation_playbook': '---\n'
                               '- name: Validate 4.11\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check rescue log\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/rescue_activated.log\n'
                               '      register: r_st\n'
                               '    - name: Check always log\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/always_cleanup.log\n'
                               '      register: a_st\n'
                               '    - name: Assert both logs exist\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - r_st.stat.exists\n'
                               '          - a_st.stat.exists\n',
        'xp': 200},
    {   'difficulty': 'Advanced',
        'explanation': '### Rolling Updates with `serial`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Zero-Downtime Rolling Wave\n'
                       '  hosts: all\n'
                       '  serial: 2\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Deploy rolling update batch\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /tmp/rolling_batch.txt\n'
                       '        content: "Batch Deployed on {{ ansible_hostname }}\n'
                       '"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/rolling.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: serial keyword',
                         'text': '--- \\n- name: Rolling update\\n  hosts: all\\n  serial: 2\\n  gather_facts: '
                                 'true\\n  tasks: ...'}],
        'id': 'l4-12-rolling-updates',
        'inspect_cmd': "ansible all -m command -a 'cat /tmp/rolling_batch.txt'",
        'module': 'lvl4',
        'primer': {   'concept': 'The `serial` directive divides inventory into batches, executing the entire play on '
                                 'batch 1 before moving to batch 2. If batch 1 encounters an error, the play halts, '
                                 'safeguarding the rest of the fleet.',
                      'demo_code': '---\n'
                                   '- name: Progressive Zero-Downtime Rolling Update\n'
                                   '  hosts: <target_hosts>\n'
                                   '  serial: 2\n'
                                   '  gather_facts: true\n'
                                   '  tasks:\n'
                                   '    - name: Update batch of servers\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/version.txt\n'
                                   '        content: "Updated on {{ ansible_hostname }}\\n"\n',
                      'quick_tip': 'serial: 2 ensures only 2 hosts execute the play at a time. The next batch only '
                                   'begins after the previous batch completes.',
                      'syntax_breakdown': [   {   'element': 'serial: 2',
                                                  'role': 'Restricts execution to batches of 2 nodes at a time'},
                                              {'element': "serial: [1, 2, '50%']", 'role': 'Canary progression list'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 4.12\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge batch file\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/rolling_batch.txt\n'
                          '        state: absent\n',
        'scenario': 'By default, Ansible runs each task across all targeted hosts simultaneously. If you restart a '
                    'database or web server on all nodes at the same time, you create total service downtime!\n'
                    '\n'
                    'The `serial:` keyword controls batching:\n'
                    '- `serial: 2`: Updates 2 nodes at a time. The next batch of 2 nodes only starts after the '
                    'previous batch completes all tasks!\n'
                    '- `serial: [1, 2, "100%"]`: Progressive canary rollout (first 1 node, then 2, then remainder).\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/rolling.yml` targeting `all` nodes with `serial: 2`. Add a task that places '
                    '`/tmp/rolling_batch.txt` containing `Batch Deployed on {{ ansible_hostname }}\\n`."*',
        'solution_code': '---\n'
                         '- name: Zero-Downtime Rolling Wave\n'
                         '  hosts: all\n'
                         '  serial: 2\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Deploy rolling update batch\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /tmp/rolling_batch.txt\n'
                         '        content: "Batch Deployed on {{ ansible_hostname }}\n'
                         '"\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/rolling.yml',
        'tasks': [   '1. Author /ansible/rolling.yml targeting all hosts.',
                     '2. Set serial: 2 at the play level.',
                     '3. Deploy /tmp/rolling_batch.txt across all nodes.',
                     '4. Run ansible-playbook /ansible/rolling.yml and observe the 3 sequential batches of 2 nodes.'],
        'title': 'Lesson 4.12: Zero-Downtime Operations — Rolling Waves with serial',
        'validation_playbook': '---\n'
                               '- name: Validate 4.12\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check batch file\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/rolling_batch.txt\n'
                               '      register: b_st\n'
                               '    - name: Assert exists\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - b_st.stat.exists\n',
        'xp': 200},
    {   'difficulty': 'Heroic',
        'explanation': '### The Capstone Deployment Pipeline\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Production Canary Deployment Pipeline\n'
                       '  hosts: all\n'
                       '  serial:\n'
                       '    - 2\n'
                       '    - "100%"\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Deploy application with rollback protection\n'
                       '      block:\n'
                       '        - name: Deploy datastream configuration\n'
                       '          ansible.builtin.copy:\n'
                       '            dest: /etc/datastream.conf\n'
                       '            content: "cluster_node={{ ansible_hostname }}\n'
                       'os_family={{ ansible_os_family }}\n'
                       'stream_active=true\n'
                       '"\n'
                       '          notify: restart cron\n'
                       '      rescue:\n'
                       '        - name: Record failure audit\n'
                       '          ansible.builtin.copy:\n'
                       '            dest: /var/log/canary_rescue.log\n'
                       '            content: "Deployment rescued\n'
                       '"\n'
                       '\n'
                       '  handlers:\n'
                       '    - name: restart cron\n'
                       '      ansible.builtin.service:\n'
                       '        name: cron\n'
                       '        state: restarted\n'
                       '      ignore_errors: true\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/canary_deploy.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Canary pipeline structure',
                         'text': "hosts: all\\nserial:\\n  - 2\\n  - '100%'\\ngather_facts: true\\ntasks:\\n  - "
                                 'block:\\n      - ansible.builtin.copy:\\n          dest: '
                                 '/etc/datastream.conf\\n          content: "cluster_node={{ ansible_hostname '
                                 '}}\\nos_family={{ ansible_os_family }}\\nstream_active=true\\n"\\n        notify: '
                                 'restart cron\\n    rescue:\\n      - ansible.builtin.copy:\\n          dest: '
                                 '/var/log/canary_rescue.log\\n          content: "failed\\n"\\nhandlers:\\n  - name: '
                                 'restart cron\\n    ansible.builtin.service:\\n      name: cron\\n      state: '
                                 'restarted'}],
        'id': 'l4-13-capstone-launch',
        'is_capstone': True,
        'capstone_type': 'capstone',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/datastream.conf'",
        'module': 'lvl4',
        'reset_playbook': '---\n'
                          '- name: Reset Capstone\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge datastream config\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/datastream.conf\n'
                          '        state: absent\n',
        'scenario': '🚨 **SEVERITY 1 CAPSTONE: LAUNCHING THE PRODUCTION DATASTREAM CLUSTER**\n'
                    'DataForge Systems is rolling out the core **DataStream v4** telemetry release across the entire '
                    '6-node heterogeneous cluster. The Incident Commander and VP of Infrastructure are watching.\n'
                    '\n'
                    'Requirements for `/ansible/canary_deploy.yml`:\n'
                    '1. **Canary Batches**: Use `serial: [2, "100%"]` so 2 canary nodes deploy first, followed by the '
                    'rest.\n'
                    '2. **Template Configuration**: Render `/etc/datastream.conf` on every node with content:\n'
                    '   `cluster_node={{ ansible_hostname }}\\nos_family={{ ansible_os_family '
                    '}}\\nstream_active=true\\n`\n'
                    '3. **Event-Driven Daemon Reload**: Notify handler `restart cron` to register the new telemetry '
                    'cron hook.\n'
                    '4. **Resilient Verification**: Wrap health check in a `block` with `rescue` fallback logging to '
                    '`/var/log/canary_rescue.log` if anything fails.\n'
                    '5. **Zero-Downtime Verification**: All 6 nodes must report operational status!',
        'solution_code': '---\n'
                         '- name: Production Canary Deployment Pipeline\n'
                         '  hosts: all\n'
                         '  serial:\n'
                         '    - 2\n'
                         '    - "100%"\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Deploy application with rollback protection\n'
                         '      block:\n'
                         '        - name: Deploy datastream configuration\n'
                         '          ansible.builtin.copy:\n'
                         '            dest: /etc/datastream.conf\n'
                         '            content: "cluster_node={{ ansible_hostname }}\n'
                         'os_family={{ ansible_os_family }}\n'
                         'stream_active=true\n'
                         '"\n'
                         '          notify: restart cron\n'
                         '      rescue:\n'
                         '        - name: Record failure audit\n'
                         '          ansible.builtin.copy:\n'
                         '            dest: /var/log/canary_rescue.log\n'
                         '            content: "Deployment rescued\n'
                         '"\n'
                         '\n'
                         '  handlers:\n'
                         '    - name: restart cron\n'
                         '      ansible.builtin.service:\n'
                         '        name: cron\n'
                         '        state: restarted\n'
                         '      ignore_errors: true\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/canary_deploy.yml',
        'tasks': [   '1. Author /ansible/canary_deploy.yml targeting all hosts with gather_facts: true.',
                     "2. Enforce serial: [2, '100%'] canary batches.",
                     '3. Deploy /etc/datastream.conf with required host and OS facts.',
                     '4. Wire notify to restart cron handler.',
                     '5. Protect deployment with block/rescue resilience.',
                     '6. Execute canary_deploy.yml and claim the Principal Hero badge!'],
        'title': 'Lesson 4.13: CAPSTONE: Incident #2089 — Production Canary Deployment Pipeline',
        'validation_playbook': '---\n'
                               '- name: Validate Capstone\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check datastream config\n'
                               '      ansible.builtin.command: cat /etc/datastream.conf\n'
                               '      register: d_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'cluster_node=\' in d_res.stdout"\n'
                               '          - "\'os_family=\' in d_res.stdout"\n'
                               '          - "\'stream_active=true\' in d_res.stdout"\n',
        'xp': 300},
    {   'difficulty': 'Advanced',
        'explanation': '### Grand Capstone: End-to-End Production Provisioning Pipeline\n'
                       '1. Append host to `/ansible/inventory.ini`:\n'
                       '```ini\n'
                       '[edge]\n'
                       'node7-alpine ansible_host=node7-alpine ansible_python_interpreter=/usr/bin/python3\n'
                       '```\n'
                       '2. Author `/ansible/provision_client.yml`:\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Production Client Commissioning Pipeline\n'
                       '  hosts: edge\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Ensure wheel group exists\n'
                       '      ansible.builtin.group:\n'
                       '        name: wheel\n'
                       '        state: present\n'
                       '    - name: Create deployer user\n'
                       '      ansible.builtin.user:\n'
                       '        name: deployer\n'
                       '        group: wheel\n'
                       '        shell: /bin/bash\n'
                       '        create_home: true\n'
                       '        state: present\n'
                       '    - name: Configure passwordless sudo\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /etc/sudoers.d/deployer\n'
                       '        content: "deployer ALL=(ALL) NOPASSWD: ALL\n"\n'
                       "        mode: '0440'\n"
                       '    - name: Install Nginx web server\n'
                       '      community.general.apk:\n'
                       '        name: nginx\n'
                       '        state: present\n'
                       '    - name: Deploy index page\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /var/lib/nginx/html/index.html\n'
                       '        content: "<h1>DataForge Edge Node Online: {{ ansible_hostname }}</h1>\n"\n'
                       "        mode: '0644'\n"
                       '    - name: Start Nginx web service\n'
                       '      ansible.builtin.service:\n'
                       '        name: nginx\n'
                       '        state: started\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/provision_client.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: inventory.ini enrollment',
                         'text': 'Add this to /ansible/inventory.ini:\n[edge]\nnode7-alpine ansible_host=node7-alpine ansible_python_interpreter=/usr/bin/python3'},
                     {   'level': 'Hint 2: sudoers and user creation',
                         'text': 'user: name=deployer group=wheel shell=/bin/bash\ncopy: dest=/etc/sudoers.d/deployer content="deployer ALL=(ALL) NOPASSWD: ALL\\n" mode=\'0440\''},
                     {   'level': 'Hint 3: Nginx on Alpine',
                         'text': 'community.general.apk: name=nginx state=present\ncopy: dest=/var/lib/nginx/html/index.html content="<h1>DataForge Edge Node Online</h1>\\n"\nservice: name=nginx state=started'}],
        'id': 'l4-14-grand-capstone',
        'is_capstone': True,
        'capstone_type': 'grand_capstone',
        'inspect_cmd': 'curl -s http://node7-alpine/',
        'module': 'lvl4',
        'reset_playbook': '---\n'
                          '- name: Reset 4.14 Inventory\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Reset inventory.ini edge entry\n'
                          '      ansible.builtin.lineinfile:\n'
                          '        path: /ansible/inventory.ini\n'
                          "        regexp: '^(node7-alpine|\\[edge\\])'\n"
                          '        state: absent\n'
                          '- name: Reset 4.14 Edge Node State\n'
                          '  hosts: node7-alpine\n'
                          '  gather_facts: false\n'
                          '  vars:\n'
                          '    ansible_python_interpreter: /usr/bin/python3\n'
                          '  tasks:\n'
                          '    - name: Stop nginx\n'
                          '      ansible.builtin.command: pkill nginx\n'
                          '      ignore_errors: true\n'
                          '    - name: Purge nginx and pcre2\n'
                          '      community.general.apk:\n'
                          '        name:\n'
                          '          - nginx\n'
                          '          - pcre2\n'
                          '        state: absent\n'
                          '      ignore_errors: true\n'
                          '    - name: Remove deployer user\n'
                          '      ansible.builtin.user:\n'
                          '        name: deployer\n'
                          '        state: absent\n'
                          '        remove: true\n'
                          '      ignore_errors: true\n'
                          '    - name: Remove sudoers and html drop-ins\n'
                          '      ansible.builtin.file:\n'
                          '        path: "{{ item }}"\n'
                          '        state: absent\n'
                          '      loop:\n'
                          '        - /etc/sudoers.d/deployer\n'
                          '        - /var/lib/nginx/html/index.html\n'
                          '      ignore_errors: true\n'
                          '    - name: Restore default nginx server config\n'
                          '      ansible.builtin.copy:\n'
                          '        dest: /etc/nginx/http.d/default.conf\n'
                          '        content: "server {\\n    listen 80 default_server;\\n    root /var/lib/nginx/html;\\n    index index.html;\\n}\\n"\n'
                          "        mode: '0644'\n"
                          '      ignore_errors: true\n',
        'scenario': 'Welcome to the **Grand Capstone Mission**!\n\n'
                    'A brand-new edge computing node (`node7-alpine`) has just arrived on the operations network.\n\n'
                    'As the Senior Systems Administrator, you are tasked with taking this unmanaged machine to fully hardened, '
                    'compliant production readiness in a single automated lifecycle:\n\n'
                    '1. **Enroll Host**: Append group `[edge]` with `node7-alpine ansible_host=node7-alpine ansible_python_interpreter=/usr/bin/python3` to `/ansible/inventory.ini`.\n'
                    '2. **Author Playbook**: Create `/ansible/provision_client.yml` targeting `edge` with `gather_facts: true`.\n'
                    '3. **Create Operations User**: Ensure group `wheel` exists and create user `deployer` with group `wheel` and `/bin/bash` shell.\n'
                    '4. **Configure Sudoers**: Write `/etc/sudoers.d/deployer` granting `deployer ALL=(ALL) NOPASSWD: ALL` with mode `0440`.\n'
                    '5. **Install Nginx**: Use `community.general.apk` (or `package`) to install package `nginx`.\n'
                    '6. **Deploy Landing Page**: Write `/var/lib/nginx/html/index.html` with content `<h1>DataForge Edge Node Online</h1>`.\n'
                    '7. **Start Daemon**: Ensure service `nginx` is `started`.\n'
                    '8. **Execute**: Run `ansible-playbook /ansible/provision_client.yml` to complete your commissioning!',
        'solution_code': '---\n'
                         '- name: Production Client Commissioning Pipeline\n'
                         '  hosts: edge\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Ensure wheel group exists\n'
                         '      ansible.builtin.group:\n'
                         '        name: wheel\n'
                         '        state: present\n'
                         '    - name: Create deployer user\n'
                         '      ansible.builtin.user:\n'
                         '        name: deployer\n'
                         '        group: wheel\n'
                         '        shell: /bin/bash\n'
                         '        create_home: true\n'
                         '        state: present\n'
                         '    - name: Configure passwordless sudo\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /etc/sudoers.d/deployer\n'
                         '        content: "deployer ALL=(ALL) NOPASSWD: ALL\n"\n'
                         "        mode: '0440'\n"
                         '    - name: Install Nginx web server\n'
                         '      community.general.apk:\n'
                         '        name: nginx\n'
                         '        state: present\n'
                         '    - name: Deploy index page\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /var/lib/nginx/html/index.html\n'
                         '        content: "<h1>DataForge Edge Node Online</h1>\n"\n'
                         "        mode: '0644'\n"
                         '    - name: Start Nginx web service\n'
                         '      ansible.builtin.service:\n'
                         '        name: nginx\n'
                         '        state: started\n',
        'solution_type': 'playbook',
        'target': 'edge',
        'target_file': '/ansible/provision_client.yml',
        'tasks': [   '1. Enroll node7-alpine in /ansible/inventory.ini under group [edge].',
                     '2. Author /ansible/provision_client.yml targeting group edge.',
                     '3. Create group wheel and administrative user deployer with shell /bin/bash.',
                     '4. Deploy /etc/sudoers.d/deployer with passwordless sudo (mode 0440).',
                     '5. Install package nginx and deploy /var/lib/nginx/html/index.html.',
                     '6. Start the nginx service daemon.',
                     '7. Execute ansible-playbook /ansible/provision_client.yml and achieve 100% verification!'],
        'title': 'Lesson 4.14: GRAND CAPSTONE: Full Fleet Commissioning — End-to-End Linux Client Provisioning',
        'validation_playbook': '---\n'
                               '- name: Validate 4.14 Inventory\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check inventory.ini\n'
                               '      ansible.builtin.command: grep -E "node7-alpine" /ansible/inventory.ini\n'
                               '      register: inv_chk\n'
                               '    - name: Assert inventory entry\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'node7-alpine\' in inv_chk.stdout"\n'
                               '- name: Validate 4.14 Edge Provisioning State\n'
                               '  hosts: node7-alpine\n'
                               '  gather_facts: false\n'
                               '  vars:\n'
                               '    ansible_python_interpreter: /usr/bin/python3\n'
                               '  tasks:\n'
                               '    - name: Check deployer user\n'
                               '      ansible.builtin.command: id deployer\n'
                               '      register: user_chk\n'
                               '    - name: Assert deployer exists\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'deployer\' in user_chk.stdout"\n'
                               '    - name: Check sudoers file\n'
                               '      ansible.builtin.command: cat /etc/sudoers.d/deployer\n'
                               '      register: sudo_chk\n'
                               '    - name: Assert sudoers content\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'deployer ALL=(ALL) NOPASSWD: ALL\' in sudo_chk.stdout"\n'
                               '    - name: Check nginx process\n'
                               '      ansible.builtin.command: pgrep nginx\n'
                               '      register: nginx_chk\n'
                               '    - name: Assert nginx running\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "nginx_chk.stdout != \'\'"\n'
                               '    - name: Test HTTP response from nginx\n'
                               '      ansible.builtin.command: wget -qO- http://127.0.0.1/\n'
                               '      register: http_chk\n'
                               '    - name: Assert web page rendered\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'DataForge\' in http_chk.stdout or \'Edge\' in http_chk.stdout"\n',
        'xp': 500}]

