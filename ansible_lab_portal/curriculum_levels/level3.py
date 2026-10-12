# Level 3: Dynamic Logic — Variables, Facts, Loops & Conditionals (Lessons 3.1 to 3.12)

LEVEL3_EXERCISES = [   {   'difficulty': 'Intermediate',
        'explanation': '### Referencing Variables with Jinja2\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Configure Port Variable\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  vars:\n'
                       '    service_port: 8080\n'
                       '  tasks:\n'
                       '    - name: Write port configuration\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /etc/dataforge_port.conf\n'
                       '        content: "PORT={{ service_port }}\n'
                       '"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/vars.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: vars section',
                         'text': 'vars:\\n  service_port: 8080\\ntasks:\\n  - name: Write port\\n    '
                                 'ansible.builtin.copy:\\n      dest: /etc/dataforge_port.conf\\n      content: '
                                 '"PORT={{ service_port }}\\n"'}],
        'id': 'l3-1-vars-section',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/dataforge_port.conf'",
        'module': 'lvl3',
        'primer': {   'concept': 'Variables separate configuration values from playbook logic. Variables defined in '
                                 '`vars:` are interpolated inside strings using double curly braces: `{{ var_name }}`.',
                      'demo_code': '---\n'
                                   '- name: Parameterized Playbook with Variables\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  vars:\n'
                                   '    custom_setting_name: <setting_value>\n'
                                   '  tasks:\n'
                                   '    - name: Write configuration using variable\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/config.conf\n'
                                   '        content: "PARAM={{ custom_setting_name }}\\n"\n',
                      'quick_tip': 'Inside Jinja2 curly braces {{ variable_name }}, Ansible looks up variables defined '
                                   'under vars:.',
                      'syntax_breakdown': [   {   'element': 'vars:',
                                                  'role': 'Section defining play-scoped variable key-value pairs'},
                                              {'element': 'service_port: 8080', 'role': 'Key and value definition'},
                                              {   'element': '"PORT={{ service_port }}"',
                                                  'role': 'Jinja2 variable interpolation inside quotes'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.1\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge port file\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/dataforge_port.conf\n'
                          '        state: absent\n',
        'scenario': 'Welcome to **Level 3: Dynamic Logic**! Hardcoding values like ports, versions, and paths across '
                    'dozens of plays makes automation brittle.\n'
                    '\n'
                    'Ansible allows declaring variables directly inside a play under the `vars:` section, referenced '
                    'using Jinja2 syntax `{{ variable_name }}`.\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"Create `/ansible/vars.yml` targeting `all` nodes. Declare a variable `service_port: 8080`. '
                    'Use `ansible.builtin.copy` to write `/etc/dataforge_port.conf` with content `PORT={{ service_port '
                    '}}\\n`."*',
        'solution_code': '---\n'
                         '- name: Configure Port Variable\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  vars:\n'
                         '    service_port: 8080\n'
                         '  tasks:\n'
                         '    - name: Write port configuration\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /etc/dataforge_port.conf\n'
                         '        content: "PORT={{ service_port }}\n'
                         '"\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/vars.yml',
        'tasks': [   '1. Author /ansible/vars.yml targeting all hosts.',
                     '2. Define the vars: section with service_port set to 8080.',
                     '3. Reference {{ service_port }} in the copy task.',
                     '4. Execute ansible-playbook /ansible/vars.yml.'],
        'title': 'Lesson 3.1: Playbook Variables — Declaring & Referencing vars',
        'validation_playbook': '---\n'
                               '- name: Validate 3.1\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check port file\n'
                               '      ansible.builtin.command: cat /etc/dataforge_port.conf\n'
                               '      register: p_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'PORT=8080\' in p_res.stdout"\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Decoupled Variables with `vars_files`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Load External Configuration Variables\n'
                       '  hosts: ubuntu\n'
                       '  gather_facts: false\n'
                       '  vars_files:\n'
                       '    - /ansible/app_vars.yml\n'
                       '  tasks:\n'
                       '    - name: Write application environment file\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /tmp/app_config.env\n'
                       '        content: "TIER={{ env_tier }}\n'
                       'DB_PORT={{ db_port }}\n'
                       '"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/site_vars.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: vars_files directive',
                         'text': 'vars_files:\\n  - /ansible/app_vars.yml\\ntasks:\\n  - name: Write env\\n    '
                                 'ansible.builtin.copy:\\n      dest: /tmp/app_config.env\\n      content: "TIER={{ '
                                 'env_tier }}\\nDB_PORT={{ db_port }}\\n"'}],
        'id': 'l3-2-vars-files',
        'inspect_cmd': "ansible ubuntu -m command -a 'cat /tmp/app_config.env'",
        'module': 'lvl3',
        'primer': {   'concept': 'The `vars_files` directive loads external YAML files containing key-value '
                                 'dictionaries. This decouples infrastructure code from environment-specific '
                                 'configuration, allowing the same playbook to run against dev, staging, or '
                                 'production.\n\n'
                                 '💡 **Golden Rule**: An external variables file is a pure YAML dictionary (`key: value`). '
                                 'Do **not** wrap its contents in a top-level `vars:` key.',
                      'sample_files': [   {   'badge': '📄 External Var File',
                                              'desc': 'Plain YAML dictionary (note: raw key-value pairs, NO "vars:" wrapper key):',
                                              'path': '/ansible/app_vars.yml',
                                              'code': 'env_tier: production\ndb_port: 5432\napi_endpoint: "https://api.dataforge.internal"\n'}],
                      'demo_code': '---\n'
                                   '- name: External Variable File Separation\n'
                                   '  hosts: ubuntu\n'
                                   '  gather_facts: false\n'
                                   '  vars_files:\n'
                                   '    - /ansible/app_vars.yml\n'
                                   '  tasks:\n'
                                   '    - name: Apply loaded external variables\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /tmp/app_config.env\n'
                                   '        content: "TIER={{ env_tier }}\n'
                                   'DB_PORT={{ db_port }}\n"\n',
                      'quick_tip': 'vars_files loads key-value pairs from external YAML files. Never write "vars:" inside the external file itself!',
                      'syntax_breakdown': [   {   'element': 'env_tier: production',
                                                  'role': 'Key-value variable defined inside external file (/ansible/app_vars.yml)'},
                                              {   'element': 'vars_files:',
                                                  'role': 'List of external YAML files to load into play variable scope'},
                                              {'element': '- /ansible/app_vars.yml', 'role': 'Path to variables file'},
                                              {   'element': '{{ env_tier }}',
                                                  'role': 'Variable resolved from the external file'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.2\n'
                          '  hosts: ubuntu\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove app_config.env\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/app_config.env\n'
                          '        state: absent\n',
        'scenario': 'In Lesson 3.1, variables were declared inline in the playbook. In enterprise projects, variables '
                    'are separated into external YAML files (e.g., `prod_vars.yml`, `staging_vars.yml`) and included '
                    'via `vars_files:`.\n'
                    '\n'
                    'The Platform Lead asks:\n'
                    '> *"We have placed an external variables file at `/ansible/app_vars.yml` containing `env_tier: '
                    'production` and `db_port: 5432`. Create `/ansible/site_vars.yml` targeting the `ubuntu` group, '
                    'load `/ansible/app_vars.yml` using `vars_files:`, and generate `/tmp/app_config.env` with content '
                    '`TIER={{ env_tier }}\\nDB_PORT={{ db_port }}\\n`."*',
        'setup_playbook': '---\n'
                          '- name: Seed app_vars.yml\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Write external vars file\n'
                          '      ansible.builtin.copy:\n'
                          '        dest: /ansible/app_vars.yml\n'
                          '        content: "env_tier: production\n'
                          'db_port: 5432\n'
                          '"\n',
        'solution_code': '---\n'
                         '- name: Load External Configuration Variables\n'
                         '  hosts: ubuntu\n'
                         '  gather_facts: false\n'
                         '  vars_files:\n'
                         '    - /ansible/app_vars.yml\n'
                         '  tasks:\n'
                         '    - name: Write application environment file\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /tmp/app_config.env\n'
                         '        content: "TIER={{ env_tier }}\n'
                         'DB_PORT={{ db_port }}\n'
                         '"\n',
        'solution_type': 'playbook',
        'target': 'ubuntu',
        'target_file': '/ansible/site_vars.yml',
        'tasks': [   '1. Author /ansible/site_vars.yml targeting group ubuntu.',
                     '2. Use the vars_files directive to load /ansible/app_vars.yml.',
                     '3. Render /tmp/app_config.env using variables {{ env_tier }} and {{ db_port }}.',
                     '4. Run ansible-playbook /ansible/site_vars.yml.'],
        'title': 'Lesson 3.2: External Data Separation — Loading Variables with vars_files',
        'validation_playbook': '---\n'
                               '- name: Validate 3.2\n'
                               '  hosts: ubuntu\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check app_config.env\n'
                               '      ansible.builtin.command: cat /tmp/app_config.env\n'
                               '      register: e_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'TIER=production\' in e_res.stdout"\n'
                               '          - "\'DB_PORT=5432\' in e_res.stdout"\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Looping Over Lists\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Batch Scaffold Directories\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Create dataforge log directories\n'
                       '      ansible.builtin.file:\n'
                       '        path: "{{ item }}"\n'
                       '        state: directory\n'
                       "        mode: '0755'\n"
                       '      loop:\n'
                       '        - /var/log/dataforge/audit\n'
                       '        - /var/log/dataforge/apps\n'
                       '        - /var/log/dataforge/metrics\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/loop_lists.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: loop directive',
                         'text': 'path: "{{ item }}"\\nloop:\\n  - /var/log/dataforge/audit\\n  - '
                                 '/var/log/dataforge/apps\\n  - /var/log/dataforge/metrics'}],
        'id': 'l3-3-loop-lists',
        'inspect_cmd': "ansible all -m command -a 'ls -ld /var/log/dataforge/*'",
        'module': 'lvl3',
        'primer': {   'concept': 'The `loop:` keyword iterates over a list of items, executing the task once for each '
                                 'element. The current element is accessible as `{{ item }}`.',
                      'demo_code': '---\n'
                                   '- name: Batch Task with Simple List Loop\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Create multiple directories in a single task\n'
                                   '      ansible.builtin.file:\n'
                                   '        path: "{{ item }}"\n'
                                   '        state: directory\n'
                                   "        mode: '0755'\n"
                                   '      loop:\n'
                                   '        - /path/to/first_dir\n'
                                   '        - /path/to/second_dir\n',
                      'quick_tip': 'The loop: directive executes the task once for each element in the list, '
                                   'accessible as {{ item }}.',
                      'syntax_breakdown': [   {'element': 'loop: [ ... ]', 'role': 'List of values to iterate over'},
                                              {   'element': '"{{ item }}"',
                                                  'role': 'Built-in variable holding the current iteration item'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.3\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove directories\n'
                          '      ansible.builtin.file:\n'
                          '        path: /var/log/dataforge\n'
                          '        state: absent\n',
        'scenario': 'In Lesson 2.6, you scaffolded 2 directories using 2 separate tasks. But what if you needed to '
                    "create 10 directories or create 5 files? Writing 10 repetitive tasks violates DRY (Don't Repeat "
                    'Yourself).\n'
                    '\n'
                    'Ansible provides the `loop:` directive. Inside the task, the current item is referenced as `{{ '
                    'item }}`.\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"Create `/ansible/loop_lists.yml` targeting `all` nodes. Use a single `ansible.builtin.file` '
                    'task with `loop:` to create these 3 directories with mode `0755`:*\n'
                    '- `/var/log/dataforge/audit`\n'
                    '- `/var/log/dataforge/apps`\n'
                    '- `/var/log/dataforge/metrics`"*"*',
        'solution_code': '---\n'
                         '- name: Batch Scaffold Directories\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Create dataforge log directories\n'
                         '      ansible.builtin.file:\n'
                         '        path: "{{ item }}"\n'
                         '        state: directory\n'
                         "        mode: '0755'\n"
                         '      loop:\n'
                         '        - /var/log/dataforge/audit\n'
                         '        - /var/log/dataforge/apps\n'
                         '        - /var/log/dataforge/metrics\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/loop_lists.yml',
        'tasks': [   '1. Author /ansible/loop_lists.yml targeting all hosts.',
                     "2. Define a single file task with state: directory and mode '0755'.",
                     '3. Use loop: with the list of 3 log directories.',
                     '4. Reference {{ item }} in the path parameter.',
                     '5. Execute ansible-playbook /ansible/loop_lists.yml.'],
        'title': 'Lesson 3.3: Iteration Power — Looping Over Simple Lists with loop',
        'validation_playbook': '---\n'
                               '- name: Validate 3.3\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check audit dir\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /var/log/dataforge/audit\n'
                               '      register: a_st\n'
                               '    - name: Check apps dir\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /var/log/dataforge/apps\n'
                               '      register: ap_st\n'
                               '    - name: Check metrics dir\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /var/log/dataforge/metrics\n'
                               '      register: m_st\n'
                               '    - name: Assert all 3 exist\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - a_st.stat.exists\n'
                               '          - ap_st.stat.exists\n'
                               '          - m_st.stat.exists\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Dictionary Loops\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Deploy Parameterized Configurations\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Deploy configuration files\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: "{{ item.dest }}"\n'
                       '        content: "{{ item.content }}"\n'
                       '        mode: "{{ item.mode }}"\n'
                       '      loop:\n'
                       '        - dest: /tmp/app1.cfg\n'
                       '          content: "service=auth\n'
                       '"\n'
                       "          mode: '0644'\n"
                       '        - dest: /tmp/app2.cfg\n'
                       '          content: "service=billing\n'
                       '"\n'
                       "          mode: '0600'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/loop_dicts.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Dictionary loop',
                         'text': 'loop:\\n  - { dest: /tmp/app1.cfg, content: "service=auth\\n", mode: \'0644\' }\\n  '
                                 '- { dest: /tmp/app2.cfg, content: "service=billing\\n", mode: \'0600\' }'}],
        'id': 'l3-4-loop-dicts',
        'inspect_cmd': "ansible all -m command -a 'ls -l /tmp/app1.cfg /tmp/app2.cfg'",
        'module': 'lvl3',
        'primer': {   'concept': 'Looping over lists of key-value dictionaries allows parameterizing complex tasks '
                                 'with multiple fields per item, accessed as `{{ item.property }}`.',
                      'demo_code': '---\n'
                                   '- name: Multi-Property Iteration with Dictionaries\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Deploy parameterized files\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: "{{ item.dest }}"\n'
                                   '        content: "{{ item.content }}"\n'
                                   '        mode: "{{ item.mode }}"\n'
                                   '      loop:\n'
                                   '        - dest: /tmp/sample1.cfg\n'
                                   '          content: "sample_value=1\\n"\n'
                                   "          mode: '0644'\n"
                                   '        - dest: /tmp/sample2.cfg\n'
                                   '          content: "sample_value=2\\n"\n'
                                   "          mode: '0600'\n",
                      'quick_tip': 'Access dictionary attributes using dot notation: {{ item.key_name }}.',
                      'syntax_breakdown': [   {   'element': 'loop: [ {dest: ..., content: ...} ]',
                                                  'role': 'Structured list of dictionary objects'},
                                              {   'element': '"{{ item.dest }}"',
                                                  'role': "Dot notation extracting 'dest' key from current item"}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.4\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge files\n'
                          '      ansible.builtin.file:\n'
                          '        path: "{{ item }}"\n'
                          '        state: absent\n'
                          '      loop:\n'
                          '        - /tmp/app1.cfg\n'
                          '        - /tmp/app2.cfg\n',
        'scenario': 'In Lesson 3.3, you looped over plain strings. But real infrastructure often requires configuring '
                    'multiple properties per item (such as username, shell, and user group).\n'
                    '\n'
                    'In Ansible, `loop:` can iterate over a list of dictionaries. You access sub-properties using dot '
                    'notation: `{{ item.name }}`, `{{ item.path }}`, `{{ item.mode }}`.\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/loop_dicts.yml` targeting `all` nodes. Use a single `ansible.builtin.copy` '
                    'task looping over dictionaries to deploy:*\n'
                    '- `/tmp/app1.cfg` with content `service=auth` and mode `0644`\n'
                    '- `/tmp/app2.cfg` with content `service=billing` and mode `0600`"*',
        'solution_code': '---\n'
                         '- name: Deploy Parameterized Configurations\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Deploy configuration files\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: "{{ item.dest }}"\n'
                         '        content: "{{ item.content }}"\n'
                         '        mode: "{{ item.mode }}"\n'
                         '      loop:\n'
                         '        - dest: /tmp/app1.cfg\n'
                         '          content: "service=auth\n'
                         '"\n'
                         "          mode: '0644'\n"
                         '        - dest: /tmp/app2.cfg\n'
                         '          content: "service=billing\n'
                         '"\n'
                         "          mode: '0600'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/loop_dicts.yml',
        'tasks': [   '1. Author /ansible/loop_dicts.yml targeting all hosts.',
                     '2. Define a loop containing 2 dictionary objects with keys: dest, content, mode.',
                     '3. Reference item.dest, item.content, item.mode in the copy task.',
                     '4. Execute ansible-playbook /ansible/loop_dicts.yml.'],
        'title': 'Lesson 3.4: Complex Iteration — Looping Over Dictionaries with item.key',
        'validation_playbook': '---\n'
                               '- name: Validate 3.4\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check app1 mode\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/app1.cfg\n'
                               '      register: a1_st\n'
                               '    - name: Check app2 mode\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/app2.cfg\n'
                               '      register: a2_st\n'
                               '    - name: Assert files and modes\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               "          - a1_st.stat.exists and a1_st.stat.mode == '0644'\n"
                               "          - a2_st.stat.exists and a2_st.stat.mode == '0600'\n",
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Facts in Playbooks\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Record Node Identity\n'
                       '  hosts: all\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Generate node identity file\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /etc/node_identity.txt\n'
                       '        content: "HOSTNAME={{ ansible_hostname }}\n'
                       'OS_FAMILY={{ ansible_os_family }}\n'
                       '"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/facts.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Facts in playbooks',
                         'text': 'gather_facts: true\\ntasks:\\n  - name: Write identity\\n    '
                                 'ansible.builtin.copy:\\n      dest: /etc/node_identity.txt\\n      content: '
                                 '"HOSTNAME={{ ansible_hostname }}\\nOS_FAMILY={{ ansible_os_family }}\\n"'}],
        'id': 'l3-5-facts-in-playbooks',
        'inspect_cmd': "ansible all -m command -a 'cat /etc/node_identity.txt'",
        'module': 'lvl3',
        'primer': {   'concept': 'When `gather_facts: true` is enabled on a play, Ansible queries remote system '
                                 'properties and exposes them as native variables like `ansible_hostname`, '
                                 '`ansible_os_family`, and `ansible_memtotal_mb`.',
                      'demo_code': '---\n'
                                   '- name: Harness Discovered System Facts\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: true\n'
                                   '  tasks:\n'
                                   '    - name: Output host identity telemetry\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/identity.txt\n'
                                   '        content: "NODE={{ ansible_hostname }}\\nOS={{ ansible_os_family }}\\n"\n',
                      'quick_tip': 'gather_facts: true interrogates remote hosts, providing variables like '
                                   'ansible_hostname and ansible_os_family.',
                      'syntax_breakdown': [   {   'element': 'gather_facts: true',
                                                  'role': 'Runs the setup module at play startup'},
                                              {   'element': '{{ ansible_hostname }}',
                                                  'role': 'Fact containing node short hostname'},
                                              {   'element': '{{ ansible_os_family }}',
                                                  'role': 'Fact grouping OS distributions (Debian, RedHat, Alpine)'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.5\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge identity\n'
                          '      ansible.builtin.file:\n'
                          '        path: /etc/node_identity.txt\n'
                          '        state: absent\n',
        'scenario': 'In Lesson 1.7, you queried facts ad-hoc with `setup`. When `gather_facts: true` is enabled in a '
                    'play, Ansible automatically populates variables prefixed with `ansible_` for every target host!\n'
                    '\n'
                    'Your task:\n'
                    '> *"Create `/ansible/facts.yml` targeting `all` nodes with `gather_facts: true`. Use '
                    '`ansible.builtin.copy` to write `/etc/node_identity.txt` containing:*\n'
                    '`HOSTNAME={{ ansible_hostname }}\\nOS_FAMILY={{ ansible_os_family }}\\n`"*"*',
        'solution_code': '---\n'
                         '- name: Record Node Identity\n'
                         '  hosts: all\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Generate node identity file\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /etc/node_identity.txt\n'
                         '        content: "HOSTNAME={{ ansible_hostname }}\n'
                         'OS_FAMILY={{ ansible_os_family }}\n'
                         '"\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/facts.yml',
        'tasks': [   '1. Author /ansible/facts.yml targeting all hosts with gather_facts: true.',
                     '2. Access the discovered facts ansible_hostname and ansible_os_family.',
                     '3. Write /etc/node_identity.txt on each node.',
                     '4. Run ansible-playbook /ansible/facts.yml.'],
        'title': 'Lesson 3.5: Dynamic Systems — Utilizing Ansible Facts in Plays',
        'validation_playbook': '---\n'
                               '- name: Validate 3.5\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Read identity\n'
                               '      ansible.builtin.command: cat /etc/node_identity.txt\n'
                               '      register: id_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'HOSTNAME=\' in id_res.stdout"\n'
                               '          - "\'OS_FAMILY=\' in id_res.stdout"\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Conditional Logic with `when`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Conditional Execution by OS\n'
                       '  hosts: all\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Create marker on Debian family hosts only\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /tmp/debian_marker.txt\n'
                       '        content: "Debian System Confirmed\n'
                       '"\n'
                       "      when: ansible_os_family == 'Debian'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/conditionals.yml\n'
                       '```',
        'hints': [{'level': 'Hint 1: when syntax', 'text': "when: ansible_os_family == 'Debian'"}],
        'id': 'l3-6-conditionals-when',
        'inspect_cmd': 'ansible all -m command -a \'ls /tmp/debian_marker.txt 2>/dev/null || echo "Skipped"\'',
        'module': 'lvl3',
        'primer': {   'concept': 'The `when:` clause allows tasks to execute conditionally based on facts or '
                                 'variables. Notice that inside `when:`, variable names do NOT use `{{ }}` braces.',
                      'demo_code': '---\n'
                                   '- name: Conditional Task Execution\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: true\n'
                                   '  tasks:\n'
                                   '    - name: Execute only on matching OS family\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /tmp/os_marker.txt\n'
                                   '        content: "Target OS matched\\n"\n'
                                   "      when: ansible_os_family == '<TargetFamily>'\n",
                      'quick_tip': 'Do NOT use {{ }} inside when: statements. Write variable names directly: when: '
                                   "ansible_os_family == 'Debian'.",
                      'syntax_breakdown': [   {'element': 'when:', 'role': 'Conditional expression evaluated per-host'},
                                              {   'element': "ansible_os_family == 'Debian'",
                                                  'role': 'Boolean comparison (true for Ubuntu & Debian)'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.6\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove marker\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/debian_marker.txt\n'
                          '        state: absent\n',
        'scenario': 'In heterogeneous clusters (Debian, RHEL, Alpine), some tasks should only execute on specific '
                    'operating systems.\n'
                    '\n'
                    'The `when:` directive evaluates boolean expressions using Python/Jinja2 logic. If the condition '
                    'is false, Ansible skips the task on that host (`skipping: [host]`).\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"Create `/ansible/conditionals.yml` targeting `all` nodes with `gather_facts: true`. Add a '
                    'task that places `/tmp/debian_marker.txt` with content `Debian System Confirmed\\n` ONLY when '
                    '`ansible_os_family == \'Debian\'`."*',
        'solution_code': '---\n'
                         '- name: Conditional Execution by OS\n'
                         '  hosts: all\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Create marker on Debian family hosts only\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /tmp/debian_marker.txt\n'
                         '        content: "Debian System Confirmed\n'
                         '"\n'
                         "      when: ansible_os_family == 'Debian'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/conditionals.yml',
        'tasks': [   '1. Author /ansible/conditionals.yml with gather_facts: true.',
                     '2. Define a copy task creating /tmp/debian_marker.txt.',
                     "3. Add the conditional when: ansible_os_family == 'Debian'.",
                     '4. Execute ansible-playbook /ansible/conditionals.yml and verify skipping on RHEL/Alpine nodes.'],
        'title': 'Lesson 3.6: Selective Execution — Conditionals with when',
        'validation_playbook': '---\n'
                               '- name: Validate 3.6\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check marker\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /tmp/debian_marker.txt\n'
                               '      register: m_st\n'
                               '    - name: Assert marker presence based on hostname\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "(inventory_hostname in [\'node1-ubuntu\', \'node2-debian\', '
                               "'node3-debian13'] and m_st.stat.exists) or (inventory_hostname not in ['node1-ubuntu', "
                               '\'node2-debian\', \'node3-debian13\'] and not m_st.stat.exists)"\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Cross-Platform Package Management\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Install Common Utilities\n'
                       '  hosts: all\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Ensure curl is present across all distros\n'
                       '      ansible.builtin.package:\n'
                       '        name: curl\n'
                       '        state: present\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/generic_package.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: package module syntax',
                         'text': 'tasks:\\n  - name: Ensure curl installed\\n    ansible.builtin.package:\\n      '
                                 'name: curl\\n      state: present'}],
        'id': 'l3-7-package-module',
        'inspect_cmd': "ansible all -m command -a 'which curl'",
        'module': 'lvl3',
        'primer': {   'concept': 'The `ansible.builtin.package` module abstracts underlying Linux package managers '
                                 '(`apt`, `yum`, `dnf`, `apk`, `pacman`). It enables cross-platform plays without '
                                 'needing custom `when:` conditions for every package installation.',
                      'demo_code': '---\n'
                                   '- name: Generic Cross-Distro Package Management\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: true\n'
                                   '  tasks:\n'
                                   '    - name: Ensure utility package is installed\n'
                                   '      ansible.builtin.package:\n'
                                   '        name: <package_name>\n'
                                   '        state: present\n',
                      'quick_tip': 'ansible.builtin.package automatically selects apt, dnf, or apk based on the '
                                   'discovered OS.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.package:',
                                                  'role': 'Universal package manager wrapper'},
                                              {'element': 'name: curl', 'role': 'Package name to manage'},
                                              {   'element': 'state: present',
                                                  'role': 'Ensures package is installed (present / absent / latest)'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.7\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'Before managing distro-specific package managers (`apt`, `dnf`, `apk`), Ansible provides the '
                    'generic `package` module.\n'
                    '\n'
                    'The `ansible.builtin.package` module acts as a universal facade: it detects the target OS and '
                    'automatically calls the appropriate package manager under the hood!\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"Target `all` nodes in `/ansible/generic_package.yml` with `gather_facts: true`. Use '
                    '`ansible.builtin.package` to ensure common utility `curl` is in `state: present`."*',
        'solution_code': '---\n'
                         '- name: Install Common Utilities\n'
                         '  hosts: all\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Ensure curl is present across all distros\n'
                         '      ansible.builtin.package:\n'
                         '        name: curl\n'
                         '        state: present\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/generic_package.yml',
        'tasks': [   '1. Author /ansible/generic_package.yml targeting all hosts with gather_facts: true.',
                     "2. Use the ansible.builtin.package module for package 'curl'.",
                     "3. Ensure state is 'present'.",
                     '4. Run ansible-playbook /ansible/generic_package.yml.'],
        'title': 'Lesson 3.7: Generic Abstraction — The package Module Across Distros',
        'validation_playbook': '---\n'
                               '- name: Validate 3.7\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check curl presence\n'
                               '      ansible.builtin.command: which curl\n'
                               '      register: c_res\n'
                               '      failed_when: c_res.rc != 0\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Multi-Distro Playbooks\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Multi-Distro Web Server Installation\n'
                       '  hosts: all\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Install apache2 on Debian family\n'
                       '      ansible.builtin.apt:\n'
                       '        name: apache2\n'
                       '        state: present\n'
                       '        update_cache: true\n'
                       "      when: ansible_os_family == 'Debian'\n"
                       '\n'
                       '    - name: Install httpd on RedHat family\n'
                       '      ansible.builtin.dnf:\n'
                       '        name: httpd\n'
                       '        state: present\n'
                       "      when: ansible_os_family == 'RedHat'\n"
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/packages.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: apt and dnf with when',
                         'text': 'tasks:\\n  - name: Install on Debian\\n    ansible.builtin.apt:\\n      name: '
                                 "apache2\\n      state: present\\n    when: ansible_os_family == 'Debian'\\n  - name: "
                                 'Install on RedHat\\n    ansible.builtin.dnf:\\n      name: httpd\\n      state: '
                                 "present\\n    when: ansible_os_family == 'RedHat'"}],
        'id': 'l3-8-multi-distro-packages',
        'inspect_cmd': 'ansible all -m shell -a \'which apache2 || which httpd || echo "Skipped"\'',
        'module': 'lvl3',
        'primer': {   'concept': 'Enterprise automation pairs OS discovery facts (`ansible_os_family`) with native '
                                 'package modules (`apt`, `dnf`) to handle distribution differences cleanly in a '
                                 'single unified playbook.',
                      'demo_code': '---\n'
                                   '- name: Heterogeneous Package Orchestration\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: true\n'
                                   '  tasks:\n'
                                   '    - name: Install on Debian family\n'
                                   '      ansible.builtin.apt:\n'
                                   '        name: <debian_package_name>\n'
                                   '        state: present\n'
                                   '        update_cache: true\n'
                                   "      when: ansible_os_family == 'Debian'\n"
                                   '\n'
                                   '    - name: Install on RedHat family\n'
                                   '      ansible.builtin.dnf:\n'
                                   '        name: <redhat_package_name>\n'
                                   '        state: present\n'
                                   "      when: ansible_os_family == 'RedHat'\n",
                      'quick_tip': 'Package names often differ across Linux distributions (e.g. apache2 on Debian vs '
                                   'httpd on RedHat).',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.apt:',
                                                  'role': 'Native Debian/Ubuntu package module'},
                                              {   'element': 'ansible.builtin.dnf:',
                                                  'role': 'Native RHEL/Fedora/Rocky/Alma package module'},
                                              {   'element': "when: ansible_os_family == '...'",
                                                  'role': 'Guards execution to compatible systems'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.8\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge apache2 on debian\n'
                          '      ansible.builtin.shell: apt-get purge -y apache2 || true\n'
                          "      when: ansible_os_family == 'Debian'\n"
                          '    - name: Purge httpd on redhat\n'
                          '      ansible.builtin.shell: dnf remove -y httpd || true\n'
                          "      when: ansible_os_family == 'RedHat'\n",
        'scenario': 'In Lesson 3.7, `curl` had the same name on all distros. But Apache HTTP server has different '
                    'package names across distributions:\n'
                    '- Debian / Ubuntu: `apache2` (managed via `ansible.builtin.apt`)\n'
                    '- RHEL / Alma / Rocky: `httpd` (managed via `ansible.builtin.dnf`)\n'
                    '\n'
                    'Write a multi-distro installation play `/ansible/packages.yml` that installs the web server '
                    'across both Debian and RedHat families using conditional tasks with `when: ansible_os_family == '
                    "'Debian'` and `when: ansible_os_family == 'RedHat'`.",
        'solution_code': '---\n'
                         '- name: Multi-Distro Web Server Installation\n'
                         '  hosts: all\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Install apache2 on Debian family\n'
                         '      ansible.builtin.apt:\n'
                         '        name: apache2\n'
                         '        state: present\n'
                         '        update_cache: true\n'
                         "      when: ansible_os_family == 'Debian'\n"
                         '\n'
                         '    - name: Install httpd on RedHat family\n'
                         '      ansible.builtin.dnf:\n'
                         '        name: httpd\n'
                         '        state: present\n'
                         "      when: ansible_os_family == 'RedHat'\n",
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/packages.yml',
        'tasks': [   '1. Author /ansible/packages.yml with gather_facts: true targeting all hosts.',
                     "2. Define Task 1: ansible.builtin.apt installing apache2 when ansible_os_family == 'Debian'.",
                     "3. Define Task 2: ansible.builtin.dnf installing httpd when ansible_os_family == 'RedHat'.",
                     '4. Execute ansible-playbook /ansible/packages.yml.'],
        'title': 'Lesson 3.8: Polyglot Fleet — Multi-Distro Package Management',
        'validation_playbook': '---\n'
                               '- name: Validate 3.8\n'
                               '  hosts: all\n'
                               '  gather_facts: true\n'
                               '  tasks:\n'
                               '    - name: Check binary\n'
                               '      ansible.builtin.shell: which apache2 || which httpd || echo "none"\n'
                               '      register: bin_res\n'
                               '    - name: Assert installed\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "(ansible_os_family in [\'Debian\', \'RedHat\'] and bin_res.stdout != '
                               '\'none\') or (ansible_os_family not in [\'Debian\', \'RedHat\'])"\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Capturing Output with `register`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Capture Kernel Version\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Query kernel release\n'
                       '      ansible.builtin.command: uname -r\n'
                       '      register: kernel_result\n'
                       '\n'
                       '    - name: Save release string\n'
                       '      ansible.builtin.copy:\n'
                       '        dest: /tmp/kernel_version.txt\n'
                       '        content: "KERNEL={{ kernel_result.stdout }}\n'
                       '"\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/kernel.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: register syntax',
                         'text': 'tasks:\\n  - name: Get kernel\\n    ansible.builtin.command: uname -r\\n    '
                                 'register: kernel_info\\n  - name: Write file\\n    ansible.builtin.copy:\\n      '
                                 'dest: /tmp/kernel_version.txt\\n      content: "KERNEL={{ kernel_info.stdout '
                                 '}}\\n"'}],
        'id': 'l3-9-register-output',
        'inspect_cmd': "ansible all -m command -a 'cat /tmp/kernel_version.txt'",
        'module': 'lvl3',
        'primer': {   'concept': 'The `register:` statement captures the entire JSON response of a task into a '
                                 'variable. You can then inspect its sub-fields: `.rc` (exit code), `.stdout` (output '
                                 'text), `.stdout_lines` (list of output lines), or `.changed`.',
                      'demo_code': '---\n'
                                   '- name: Capture and Save Runtime Output\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Execute command and capture output\n'
                                   '      ansible.builtin.command: <command_to_run>\n'
                                   '      register: command_result\n'
                                   '\n'
                                   '    - name: Store captured stdout in a file\n'
                                   '      ansible.builtin.copy:\n'
                                   '        dest: /path/to/output.txt\n'
                                   '        content: "RESULT={{ command_result.stdout }}\\n"\n',
                      'quick_tip': 'Use register: <variable_name> to save task results. Access stdout via {{ '
                                   'variable_name.stdout }}.',
                      'syntax_breakdown': [   {   'element': 'register: kernel_result',
                                                  'role': 'Stores task result dictionary in variable'},
                                              {   'element': '{{ kernel_result.stdout }}',
                                                  'role': 'Extracts standard output string of the command'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.9\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Purge kernel file\n'
                          '      ansible.builtin.file:\n'
                          '        path: /tmp/kernel_version.txt\n'
                          '        state: absent\n',
        'scenario': 'When a task runs on a target system, it returns structured data (return code `rc`, stdout '
                    '`stdout`, stderr `stderr`, changed status `changed`).\n'
                    '\n'
                    'The `register:` keyword saves this result into a named variable for use in subsequent tasks.\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"Create `/ansible/kernel.yml` targeting `all` nodes. Run `uname -r` using '
                    '`ansible.builtin.command`, register the output as `kernel_info`, and in Task 2 write '
                    '`/tmp/kernel_version.txt` with content `KERNEL={{ kernel_info.stdout }}\\n`."*',
        'solution_code': '---\n'
                         '- name: Capture Kernel Version\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Query kernel release\n'
                         '      ansible.builtin.command: uname -r\n'
                         '      register: kernel_result\n'
                         '\n'
                         '    - name: Save release string\n'
                         '      ansible.builtin.copy:\n'
                         '        dest: /tmp/kernel_version.txt\n'
                         '        content: "KERNEL={{ kernel_result.stdout }}\n'
                         '"\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/kernel.yml',
        'tasks': [   '1. Author /ansible/kernel.yml targeting all hosts.',
                     '2. Execute uname -r with command module and register as kernel_info.',
                     '3. Use copy module to write /tmp/kernel_version.txt referencing {{ kernel_info.stdout }}.',
                     '4. Execute ansible-playbook /ansible/kernel.yml.'],
        'title': 'Lesson 3.9: Capturing Runtime State — Registering Output with register',
        'validation_playbook': '---\n'
                               '- name: Validate 3.9\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Read file\n'
                               '      ansible.builtin.command: cat /tmp/kernel_version.txt\n'
                               '      register: k_res\n'
                               '    - name: Assert contents\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'KERNEL=\' in k_res.stdout"\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Reactive Execution\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Reactive Verification\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Inspect limits file existence\n'
                       '      ansible.builtin.stat:\n'
                       '        path: /etc/security/limits.conf\n'
                       '      register: limits_check\n'
                       '\n'
                       '    - name: Append verification tag if file exists\n'
                       '      ansible.builtin.lineinfile:\n'
                       '        path: /etc/security/limits.conf\n'
                       '        line: "# DataForge Limits Verified"\n'
                       '      when: limits_check.stat.exists\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/reactive.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: Reactive pattern',
                         'text': 'tasks:\\n  - name: Check file\\n    ansible.builtin.stat:\\n      path: '
                                 '/etc/security/limits.conf\\n    register: limits_check\\n  - name: Append line\\n    '
                                 "ansible.builtin.lineinfile:\\n      path: /etc/security/limits.conf\\n      line: '# "
                                 "DataForge Limits Verified'\\n    when: limits_check.stat.exists"}],
        'id': 'l3-10-reactive-when',
        'inspect_cmd': 'ansible all -m command -a \'grep "DataForge Limits" /etc/security/limits.conf 2>/dev/null || '
                       'echo "Absent"\'',
        'module': 'lvl3',
        'primer': {   'concept': 'Reactive logic inspects a target node in step 1, registers the result, and makes '
                                 'automated decisions in step 2 based on `.stat.exists`, `.rc`, or `.stdout`.',
                      'demo_code': '---\n'
                                   '- name: Reactive Decision Workflow\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Step 1 - Audit file status\n'
                                   '      ansible.builtin.stat:\n'
                                   '        path: /path/to/inspected_file\n'
                                   '      register: file_audit\n'
                                   '\n'
                                   '    - name: Step 2 - Act only if file exists\n'
                                   '      ansible.builtin.lineinfile:\n'
                                   '        path: /path/to/inspected_file\n'
                                   '        line: "<line_to_append>"\n'
                                   '      when: file_audit.stat.exists\n',
                      'quick_tip': 'Pairing register with when: <var>.stat.exists allows safely modifying files that '
                                   'only exist on certain hosts.',
                      'syntax_breakdown': [   {   'element': 'register: limits_check',
                                                  'role': 'Captures stat module dictionary'},
                                              {   'element': 'when: limits_check.stat.exists',
                                                  'role': 'Executes task only if target file was found'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.10\n'
                          '  hosts: all\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Remove verification line\n'
                          '      ansible.builtin.lineinfile:\n'
                          '        path: /etc/security/limits.conf\n'
                          '        line: "# DataForge Limits Verified"\n'
                          '        state: absent\n'
                          '      ignore_errors: true\n',
        'scenario': 'Combining `register:` with `when:` unlocks reactive automation: inspect a remote condition in '
                    'Task 1, and only run Task 2 if the condition is met.\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"Create `/ansible/reactive.yml` targeting `all` nodes:*\n'
                    '> *1. Run `ansible.builtin.stat` on `/etc/security/limits.conf` and register as `limits_check`.*\n'
                    '> *2. Use `ansible.builtin.lineinfile` to append `# DataForge Limits Verified` to '
                    '`/etc/security/limits.conf` ONLY `when: limits_check.stat.exists`."*',
        'solution_code': '---\n'
                         '- name: Reactive Verification\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Inspect limits file existence\n'
                         '      ansible.builtin.stat:\n'
                         '        path: /etc/security/limits.conf\n'
                         '      register: limits_check\n'
                         '\n'
                         '    - name: Append verification tag if file exists\n'
                         '      ansible.builtin.lineinfile:\n'
                         '        path: /etc/security/limits.conf\n'
                         '        line: "# DataForge Limits Verified"\n'
                         '      when: limits_check.stat.exists\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/reactive.yml',
        'tasks': [   '1. Author /ansible/reactive.yml targeting all hosts.',
                     '2. Use stat module to inspect /etc/security/limits.conf and register limits_check.',
                     '3. Add a lineinfile task guarded by when: limits_check.stat.exists.',
                     '4. Execute ansible-playbook /ansible/reactive.yml.'],
        'title': 'Lesson 3.10: Reactive Logic — Combining register and when',
        'validation_playbook': '---\n'
                               '- name: Validate 3.10\n'
                               '  hosts: all\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Check file\n'
                               '      ansible.builtin.stat:\n'
                               '        path: /etc/security/limits.conf\n'
                               '      register: l_st\n'
                               '    - name: Check contents\n'
                               '      ansible.builtin.command: grep "DataForge Limits Verified" '
                               '/etc/security/limits.conf\n'
                               '      register: g_res\n'
                               '      when: l_st.stat.exists\n'
                               '    - name: Assert\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - (l_st.stat.exists and g_res.rc == 0) or (not l_st.stat.exists)\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### Custom Idempotency with `changed_when`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Query Fleet Uptime Cleanly\n'
                       '  hosts: all\n'
                       '  gather_facts: false\n'
                       '  tasks:\n'
                       '    - name: Check uptime without triggering change alert\n'
                       '      ansible.builtin.command: uptime\n'
                       '      changed_when: false\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/uptime.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: changed_when syntax',
                         'text': 'tasks:\\n  - name: Query uptime\\n    ansible.builtin.command: uptime\\n    '
                                 'changed_when: false'}],
        'id': 'l3-11-changed-when',
        'inspect_cmd': 'ansible-playbook /ansible/uptime.yml',
        'module': 'lvl3',
        'primer': {   'concept': "The `changed_when:` clause overrides Ansible's default change detection. Setting "
                                 '`changed_when: false` marks read-only diagnostic commands as `ok` (green), '
                                 'maintaining accurate compliance reports.',
                      'demo_code': '---\n'
                                   '- name: Custom Idempotency & Clean Audit Reporting\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: false\n'
                                   '  tasks:\n'
                                   '    - name: Execute read-only command without triggering changed alert\n'
                                   '      ansible.builtin.command: <read_only_command>\n'
                                   '      changed_when: false\n',
                      'quick_tip': "Setting changed_when: false forces Ansible to report 'ok' (green) instead of "
                                   "'changed' (yellow) for read-only tasks.",
                      'syntax_breakdown': [   {   'element': 'changed_when: false',
                                                  'role': "Suppresses yellow 'changed' status; forces green 'ok'"}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.11\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'By default, Ansible marks `command` and `shell` tasks as `changed: [host]` every time they run, '
                    'because Ansible cannot know whether the script modified system state.\n'
                    '\n'
                    'This creates false alerts during automated audits!\n'
                    '\n'
                    'The `changed_when:` directive allows you to define custom idempotency rules:\n'
                    '- `changed_when: false`: Tell Ansible this task NEVER changes system state (read-only query).\n'
                    '- `changed_when: "\'UPGRADED\' in result.stdout"`: Mark changed only if specific text appears.\n'
                    '\n'
                    'Your assignment:\n'
                    '> *"Create `/ansible/uptime.yml` targeting `all` nodes. Run `uptime` using '
                    '`ansible.builtin.command`. Set `changed_when: false` so Ansible reports `ok: [host]` (green) '
                    'instead of `changed` (yellow)."*',
        'solution_code': '---\n'
                         '- name: Query Fleet Uptime Cleanly\n'
                         '  hosts: all\n'
                         '  gather_facts: false\n'
                         '  tasks:\n'
                         '    - name: Check uptime without triggering change alert\n'
                         '      ansible.builtin.command: uptime\n'
                         '      changed_when: false\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/uptime.yml',
        'tasks': [   '1. Author /ansible/uptime.yml targeting all hosts.',
                     '2. Invoke command module running uptime.',
                     '3. Add changed_when: false to enforce read-only reporting.',
                     '4. Run ansible-playbook /ansible/uptime.yml and verify status is green (ok) across all nodes.'],
        'title': 'Lesson 3.11: Custom Idempotency — Overriding Changed State with changed_when',
        'validation_playbook': '---\n'
                               '- name: Validate 3.11\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Run uptime playbook and capture JSON stats\n'
                               '      ansible.builtin.command: ansible-playbook /ansible/uptime.yml\n'
                               '      register: up_res\n'
                               '    - name: Assert no changes reported\n'
                               '      ansible.builtin.assert:\n'
                               '        that:\n'
                               '          - "\'changed=0\' in up_res.stdout"\n',
        'xp': 150},
    {   'difficulty': 'Intermediate',
        'explanation': '### System Assertions with `assert`\n'
                       '```yaml\n'
                       '---\n'
                       '- name: Cluster Pre-Flight Validation\n'
                       '  hosts: all\n'
                       '  gather_facts: true\n'
                       '  tasks:\n'
                       '    - name: Verify cluster hardware & OS compliance\n'
                       '      ansible.builtin.assert:\n'
                       '        that:\n'
                       '          - ansible_memtotal_mb >= 256\n'
                       "          - ansible_os_family in ['Debian', 'RedHat', 'Alpine']\n"
                       '        fail_msg: "Host does not meet minimum production specifications!"\n'
                       '        success_msg: "Pre-flight compliance passed."\n'
                       '```\n'
                       'Execute with:\n'
                       '```bash\n'
                       'ansible-playbook /ansible/polyglot_fix.yml\n'
                       '```',
        'hints': [   {   'level': 'Hint 1: assert module syntax',
                         'text': 'ansible.builtin.assert:\\n  that:\\n    - ansible_memtotal_mb >= 256\\n    - '
                                 'ansible_os_family in [\'Debian\', \'RedHat\', \'Alpine\']\\n  fail_msg: "Node failed '
                                 'minimum pre-flight specs!"'}],
        'id': 'l3-12-assert-validation',
        'inspect_cmd': 'ansible-playbook /ansible/polyglot_fix.yml',
        'module': 'lvl3',
        'primer': {   'concept': 'The `ansible.builtin.assert` module enforces preconditions before executing risky '
                                 'tasks. If any assertion in `that:` evaluates to false, Ansible fails the play '
                                 'immediately on that host and displays your `fail_msg`.',
                      'demo_code': '---\n'
                                   '- name: Pre-Flight Operational Guardrail\n'
                                   '  hosts: <target_hosts>\n'
                                   '  gather_facts: true\n'
                                   '  tasks:\n'
                                   '    - name: Validate system meets specifications\n'
                                   '      ansible.builtin.assert:\n'
                                   '        that:\n'
                                   '          - <condition_1>\n'
                                   '          - <condition_2>\n'
                                   '        fail_msg: "Pre-flight requirements not met!"\n',
                      'quick_tip': "assert tasks halt the play immediately if any condition in 'that:' evaluates to "
                                   'false.',
                      'syntax_breakdown': [   {   'element': 'ansible.builtin.assert:',
                                                  'role': 'Module asserting system conditions'},
                                              {   'element': 'that: [ cond1, cond2 ]',
                                                  'role': 'List of assertions that must all evaluate to true'},
                                              {   'element': 'fail_msg: "..."',
                                                  'role': 'Custom error diagnostic displayed upon assertion failure'}]},
        'reset_playbook': '---\n'
                          '- name: Reset 3.12\n'
                          '  hosts: localhost\n'
                          '  connection: local\n'
                          '  gather_facts: false\n'
                          '  tasks:\n'
                          '    - name: Ready\n'
                          '      ansible.builtin.debug:\n'
                          '        msg: "Ready"\n',
        'scenario': 'In Level 3, you learned variables, facts, loops, conditionals, and registered state. Now combine '
                    'them into a production pre-flight validation gate!\n'
                    '\n'
                    'The `ansible.builtin.assert` module validates that target systems satisfy minimum requirements '
                    'before deployment begins. If assertions fail, the play halts immediately with custom error '
                    'messages.\n'
                    '\n'
                    'DataForge requirements for all fleet nodes:\n'
                    '- Total RAM must be at least 256 MB (`ansible_memtotal_mb >= 256`)\n'
                    "- Node must belong to a recognized OS family (`ansible_os_family in ['Debian', 'RedHat', "
                    "'Alpine']`)\n"
                    '\n'
                    'Author `/ansible/polyglot_fix.yml` targeting `all` nodes with `gather_facts: true` and execute '
                    'the assertion.',
        'solution_code': '---\n'
                         '- name: Cluster Pre-Flight Validation\n'
                         '  hosts: all\n'
                         '  gather_facts: true\n'
                         '  tasks:\n'
                         '    - name: Verify cluster hardware & OS compliance\n'
                         '      ansible.builtin.assert:\n'
                         '        that:\n'
                         '          - ansible_memtotal_mb >= 256\n'
                         "          - ansible_os_family in ['Debian', 'RedHat', 'Alpine']\n"
                         '        fail_msg: "Host does not meet minimum production specifications!"\n'
                         '        success_msg: "Pre-flight compliance passed."\n',
        'solution_type': 'playbook',
        'target': 'all',
        'target_file': '/ansible/polyglot_fix.yml',
        'tasks': [   '1. Author /ansible/polyglot_fix.yml with gather_facts: true targeting all hosts.',
                     '2. Use ansible.builtin.assert module.',
                     '3. Enforce that ansible_memtotal_mb >= 256.',
                     "4. Enforce that ansible_os_family in ['Debian', 'RedHat', 'Alpine'].",
                     '5. Execute ansible-playbook /ansible/polyglot_fix.yml and verify all 6 nodes pass.'],
        'title': 'Lesson 3.12: Quality Assurance — Asserting System State with assert',
        'validation_playbook': '---\n'
                               '- name: Validate 3.12\n'
                               '  hosts: localhost\n'
                               '  connection: local\n'
                               '  gather_facts: false\n'
                               '  tasks:\n'
                               '    - name: Run validation playbook\n'
                               '      ansible.builtin.command: ansible-playbook /ansible/polyglot_fix.yml\n'
                               '      register: val_res\n'
                               '      failed_when: val_res.rc != 0\n',
        'xp': 150}]

