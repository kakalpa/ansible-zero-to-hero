# Ansible Zero-to-Hero & SRE Incident Simulator

<p align="center">
  <img src="ansible_lab_portal/static/icons/terminal-icon.png" width="96" height="96" alt="Ansible Lab Icon" onerror="this.style.display='none'"/>
</p>

<p align="center">
  <b>A self-hostable, interactive browser-based Ansible learning platform & production incident simulator.</b><br>
  <i>49 progressive lessons, two-stage guided pedagogy, live 6-node multi-distro fleet, real-time telemetry HUD, Monaco YAML editor, and instant cluster factory resets.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Ansible-2.16+-EE0000?style=flat-square&logo=ansible&logoColor=white" alt="Ansible"/>
  <img src="https://img.shields.io/badge/Architecture-amd64%20%7C%20arm64%20(Apple%20Silicon)-blue?style=flat-square" alt="Multi-Arch"/>
  <img src="https://img.shields.io/badge/Docker-Compose%20v2-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
</p>

---

## ⚡ Quickstart (< 60 Seconds)

### 1. Clone the repository
```bash
git clone https://github.com/your-org/ansible-zero-to-hero.git
cd ansible-zero-to-hero
```

### 2. Run Pre-Flight Diagnostic (Optional)
```bash
./lab doctor
```

### 3. Launch the Cluster
```bash
./lab start
```

Open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

---

## 🖥️ Architecture & Fleet Topology

The lab boots a genuine 6-node heterogeneous Linux cluster inside an isolated internal Docker bridge network (`ansible-net`). No simulated mock shells—every ad-hoc command and playbook executes over real SSH against real Linux operating systems:

```
                           ┌──────────────────────────────────────────────┐
                           │          Learner's Host Workstation          │
                           │   macOS (M1-M4 / Intel) | Linux | WSL2       │
                           └──────────────────────┬───────────────────────┘
                                                  │ Web UI & PTY (:8080)
                                                  ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Docker Network: ansible-net                                                            │
│                                                                                        │
│  ┌────────────────────────┐      ┌────────────────────────┐                            │
│  │     ansible-portal     │◄────►│  docker-socket-proxy   │ (Optional Read-Only Proxy) │
│  │ (FastAPI + PTY Shell)  │      │ (tecnativa/socket-proxy)│                            │
│  └───────────┬────────────┘      └───────────┬────────────┘                            │
│              │ SSH (Ed25519)                 │ Read stats / Restart containers         │
│              ├───────────────────────────────┴────────────────────────┐                │
│              ▼                                                        ▼                │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐       │
│  │     node1-ubuntu      │  │     node2-debian      │  │    node3-debian13     │       │
│  │    (Ubuntu 22.04)     │  │   (Debian 12 Bookworm)│  │   (Debian 13 Trixie)  │       │
│  │     Package: apt      │  │     Package: apt      │  │     Package: apt      │       │
│  └───────────────────────┘  └───────────────────────┘  └───────────────────────┘       │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐       │
│  │    node4-almalinux    │  │      node5-rocky      │  │     node6-alpine      │       │
│  │   (AlmaLinux 9.4)     │  │   (Rocky Linux 9.4)   │  │    (Alpine 3.22)      │       │
│  │     Package: dnf      │  │     Package: dnf      │  │     Package: apk      │       │
│  └───────────────────────┘  └───────────────────────┘  └───────────────────────┘       │
└────────────────────────────────────────────────────────────────────────────────────────┘
  ▲ Persistent Volumes:
    ├── ./workspace:/ansible/playbooks     (Author playbooks in local VS Code/Cursor)
    └── user_data:/ansible/user_data       (XP, streaks, and challenge completion state)
```

---

## 🧰 Management CLI (`./lab`)

The zero-dependency `./lab` CLI utility manages the full lifecycle of your learning environment:

| Command | Description |
| :--- | :--- |
| `./lab start` | Boots all 6 nodes and launches the web portal in the background |
| `./lab stop` | Pauses and stops all cluster containers safely |
| `./lab restart` | Restarts all services |
| `./lab status` | Displays container health, IP addresses, and real-time RAM usage |
| `./lab reset` | Restores all 6 nodes back to clean baseline state in parallel |
| `./lab logs` | Follows real-time logs from the web portal and PTY sessions |
| `./lab doctor` | Validates host requirements (Docker, RAM, CPU architecture, ports) |
| `./lab export` | Archives your authored playbooks in `./workspace` to a timestamped `.tar.gz` |
| `./lab update` | Pulls latest pre-built container images |

---

## 📚 Curriculum Roadmap (49 Progressive Lessons)

The curriculum takes learners from absolute beginner to senior production SRE across 4 distinct levels. Every lesson features a **Two-Stage Learning Model**:
1. **Concept Primer & Syntax Blueprint**: Analog, conceptual syntax scaffolding and best practices.
2. **Production Mission**: Apply the skill to diagnose, configure, or remediate the live fleet.

Learners can also activate **Challenge-Only Mode** (`Alt+M`) to skip directly to missions with a **+25% Hardcore Bonus XP**.

<details>
<summary><b>Level 1: Fleet Discovery & Ad-Hoc Orchestration (Lessons 1.1 – 1.10)</b></summary>

- **1.1 First Contact**: Run your first `ansible all -m ping` ad-hoc connectivity check.
- **1.2 Target Selection & Groups**: Filter nodes by distribution groups (`webservers`, `debian_family`).
- **1.3 Command Execution**: Execute arbitrary commands using the `command` module safely.
- **1.4 Shell vs Command**: Utilize environment variables, redirection, and pipes with the `shell` module.
- **1.5 Fact Gathering & Fleet Recon**: Query `setup` module facts to inspect kernel and OS distributions.
- **1.6 Targeted Fact Filtering**: Filter network interfaces, IP addresses, and memory statistics.
- **1.7 Ad-Hoc User & Group Auditing**: Create and audit administrative service accounts.
- **1.8 File Permission Enforcement**: Set ownership, permissions, and directory structures across distros.
- **1.9 Ansible-Doc Exploration**: Discover module options, parameters, and examples using `ansible-doc`.
- **1.10 Ad-Hoc File Staging (Copy)**: Push configuration and scripts rapidly using `copy`.
</details>

<details>
<summary><b>Level 2: Idempotent Playbooks & Handlers (Lessons 2.1 – 2.10)</b></summary>

- **2.1 First Playbook**: Structure declarative YAML plays, targets, and tasks.
- **2.2 Debug Module & Verbosity**: Print runtime facts, custom variables, and audit messages with `debug`.
- **2.3 Idempotent File Management**: Understand idempotency and the `changed` status flag.
- **2.4 Directory Hierarchy & Permissions**: Recursively enforce secure directory permissions.
- **2.5 Surgical Line & Block Inserter**: Use `blockinfile` to inject configuration blocks safely.
- **2.6 Service Orchestration & Handlers**: Trigger smart service restarts via `notify` and `handlers`.
- **2.7 Multi-Task Handler Pipelines**: Chain multiple handlers in sequence.
- **2.8 Playbook Syntax & Dry-Run**: Validate playbooks using `--syntax-check` and `--check` dry-runs.
- **2.9 Service State & Boot Enablement**: Manage service lifecycles across systemd and OpenRC with `service`.
- **2.10 Multi-Play Enterprise Pipelines**: Coordinate web, database, and monitoring tiers in a single file.
</details>

<details>
<summary><b>Level 3: Dynamic Fleets, Conditionals & Loops (Lessons 3.1 – 3.10)</b></summary>

- **3.1 Playbook Variables**: Declare and scope variables at the play, host, and group level.
- **3.2 External Variable Files**: Decouple environments using `vars_files` and secret isolation.
- **3.3 Heterogeneous OS Conditionals**: Branch playbook logic dynamically using `when: ansible_os_family == '...'`.
- **3.4 Loop Iterations**: Automate repetitive tasks using `loop` and dictionary lists.
- **3.5 Registering & Inspecting Task Output**: Capture stdout, rc, and return values using `register`.
- **3.6 Jinja2 Dynamic Templating**: Author dynamic configuration files using `template` and Jinja2 expressions.
- **3.7 Universal Package Management**: Deploy software across `apt`, `dnf`, and `apk` using `package`.
- **3.8 Prompting & Interactive Vars**: Secure sensitive interactive inputs with `vars_prompt`.
- **3.9 Complex Logic Operators**: Combine multi-condition gates (`and`, `or`, nested facts).
- **3.10 Fail Module & Guard Rails**: Halt dangerous executions using `fail` before outages occur.
</details>

<details>
<summary><b>Level 4: Enterprise SRE, Roles, Vault & Outages (Lessons 4.1 – 4.10)</b></summary>

- **4.1 Ansible Roles Architecture**: Organize modular roles with `tasks/`, `handlers/`, `defaults/`, and `templates/`.
- **4.2 Role Defaults & Variable Precedence**: Master variable override precedence across role layers.
- **4.3 Error Handling & Rescue Blocks**: Implement try/catch reliability using `block`, `rescue`, and `always`.
- **4.4 Jinja2 Template Filters**: Transform strings, IPs, lists, and hashes using advanced filters.
- **4.5 Rolling Deployments & Serial Execution**: Orchestrate zero-downtime rolling updates using `serial: 1`.
- **4.6 Delegation & Master Tasks**: Execute tasks on third-party bastions using `delegate_to`.
- **4.7 Precision Task Execution with Tags**: Target specific tasks or skip maintenance blocks with `--tags`.
- **4.8 Asynchronous & Fire-and-Forget**: Run long-running batch jobs using `async` and `poll`.
- **4.9 Galaxy Collection Integration**: Install and leverage community collections from Ansible Galaxy.
- **4.10 Ansible Vault Secret Encryption**: Encrypt sensitive passwords, keys, and tokens with `ansible-vault`.
- **Level 4 Boss Challenge — P1 Outage Incident**: Triage a cascading fleet failure across 6 nodes under pressure!
</details>

---

## 🔒 Security & Zero-Trust Hardening

This lab is engineered with security best practices for both local workstations and cloud servers:

1. **Localhost Binding by Default**: The web portal binds to `127.0.0.1:8080`. It is never exposed to the public internet by default.
2. **Ephemeral Ed25519 Dynamic Keys**: When the lab boots, it dynamically generates a fresh, unique Ed25519 SSH keypair into an ephemeral Docker volume.
3. **Optional Docker Socket Proxy**: For zero-trust environments, mount `tecnativa/docker-socket-proxy` to restrict API access strictly to container inspection and restart, completely blocking exec and volume escapes.
4. **Non-Root Playbook Authoring**: Author playbooks on your host filesystem in `./workspace` without granting elevated host permissions.

---

## 🎓 Classroom & Workshop Multi-Tenancy

Instructors can host multiple isolated student labs on a single cloud VM (e.g. 16–32 GB RAM):

```bash
# Student 01
COMPOSE_PROJECT_NAME=student01 PORTAL_PORT=8081 BIND_HOST=0.0.0.0 docker compose up -d

# Student 02
COMPOSE_PROJECT_NAME=student02 PORTAL_PORT=8082 BIND_HOST=0.0.0.0 docker compose up -d

# Student 03
COMPOSE_PROJECT_NAME=student03 PORTAL_PORT=8083 BIND_HOST=0.0.0.0 docker compose up -d
```
Each student receives their own private 6-node cluster, isolated network namespace, and dedicated web portal.

---

## 📦 Offline & Air-Gapped Bundles

To run in air-gapped classrooms or enterprise networks without internet access:

1. **On an internet-connected workstation**:
   ```bash
   git clone https://github.com/your-org/ansible-zero-to-hero.git
   cd ansible-zero-to-hero
   ./lab start && ./lab stop
   docker save $(docker compose config --images) | gzip > ansible_lab_offline_images.tar.gz
   tar -czf ansible_lab_bundle.tar.gz .
   ```

2. **On the air-gapped machine**:
   ```bash
   tar -xzf ansible_lab_bundle.tar.gz
   docker load < ansible_lab_offline_images.tar.gz
   ./lab start
   ```

---

## 💻 Hardware Requirements

| Requirement | Minimum | Recommended |
| :--- | :--- | :--- |
| **CPU** | 2 vCPUs (x86_64 or Apple Silicon M1-M4) | 4 vCPUs |
| **Memory** | 2 GB RAM (allocated to Docker) | 4 GB+ RAM |
| **Disk Space** | 3.5 GB free space | 5 GB free space |
| **OS** | macOS 12+, Linux (Ubuntu/Debian/RHEL/Arch), Windows 10/11 WSL2 | Any 64-bit OS |

---

## 🤝 Contributing & Scenario Authoring

You can author custom lessons, corporate workshops, or SRE incident simulations without modifying any core engine code. Simply create a Python file inside `custom_scenarios/` (e.g., `custom_scenarios/my_scenario.py`). The platform automatically discovers, validates, and mounts it into the web portal on boot.

### Anatomy of an Incident Scenario

Every scenario defines:
1. **Metadata & Storyline**: Realistic DevOps on-call context, problem statement, and goals.
2. **Concept Primer & Scaffolding**: Analog syntax patterns for guided learning mode.
3. **Reset Playbook**: An Ansible playbook executed to inject or plant the simulated failure condition on the live cluster.
4. **Validation Playbook**: An Ansible playbook executed by the Verification Coach to confirm whether the learner resolved the incident.
5. **Canonical Solution**: Reference playbook and post-mortem recap.

### Full Working Example: P1 Cron Backdoor Incident (`custom_scenarios/incident_rogue_cron.py`)

```python
# Place in: custom_scenarios/incident_rogue_cron.py

CUSTOM_MODULE = {
    "id": "incidents",
    "title": "Incident Response: SRE War Room Scenarios",
    "desc": "Real-world production outages and security incidents to diagnose and remediate.",
    "badge": "Incident Commander",
    "xp_per_lesson": 250
}

CUSTOM_EXERCISES = [
    {
        "id": "incident-rogue-miner",
        "module": "incidents",
        "title": "P1 Security Incident: Rogue Cron Backdoor & Fleet Remediation",
        "difficulty": "Advanced",
        "target": "ubuntu, rhel",
        "target_file": "/ansible/remediate_incident.yml",
        "scenario": (
            "🚨 **URGENT SECURITY ALERT (P1 - Critical)**\n\n"
            "The DataForge SOC detected unauthorized outbound beaconing and abnormal CPU spikes "
            "originating from `node1-ubuntu` and `node4-almalinux`.\n\n"
            "Forensics identified an unauthorized cron persistence job at `/etc/cron.d/malicious_beacon` "
            "triggering `/opt/crypto_miner.sh`.\n\n"
            "**Incident Commander Instructions:**\n"
            "> *\"Author an idempotent remediation playbook at `/ansible/remediate_incident.yml`. "
            "Permanently delete the cron file, remove the payload executable, and drop a hardened "
            "audit notice at `/etc/security/audit_notice.txt` containing 'INCIDENT_REMEDIATED=TRUE'.\"*"
        ),
        "tasks": [
            "1. Target both affected groups (ubuntu, rhel).",
            "2. Idempotently delete /etc/cron.d/malicious_beacon (state: absent).",
            "3. Idempotently delete /opt/crypto_miner.sh (state: absent).",
            "4. Deploy /etc/security/audit_notice.txt containing 'INCIDENT_REMEDIATED=TRUE' (mode: 0644)."
        ],
        "primer": {
            "concept": (
                "Incident remediation in production fleet orchestration requires idempotency. "
                "Using ansible.builtin.file with state: absent guarantees that threat artifacts are "
                "eradicated without failing if a node was already remediated."
            ),
            "demo_code": (
                "---\n"
                "- name: Enterprise Fleet Incident Containment\n"
                "  hosts: <compromised_hosts>\n"
                "  gather_facts: false\n"
                "  tasks:\n"
                "    - name: Purge malicious persistence artifact\n"
                "      ansible.builtin.file:\n"
                "        path: /path/to/threat_artifact\n"
                "        state: absent\n\n"
                "    - name: Enforce security compliance token\n"
                "      ansible.builtin.copy:\n"
                "        dest: /etc/security/audit_token\n"
                "        content: \"AUDIT_VERIFIED=TRUE\\n\"\n"
                "        mode: '0644'\n"
            ),
            "quick_tip": "Always use state: absent rather than rm -f commands. The file module is idempotent and cross-distro safe.",
            "syntax_breakdown": [
                {"element": "hosts: ubuntu, rhel", "role": "Targets multiple heterogeneous distro groups simultaneously"},
                {"element": "state: absent", "role": "Idempotently deletes the target file or directory if it exists"},
                {"element": "mode: '0644'", "role": "Enforces secure POSIX permissions on newly deployed compliance artifacts"}
            ]
        },
        "hints": [
            {
                "level": "Hint 1: Targeting Multiple Groups",
                "text": "In your playbook header, specify multiple groups: `hosts: ubuntu, rhel`."
            },
            {
                "level": "Hint 2: Idempotent Deletion",
                "text": "Use `ansible.builtin.file` with `state: absent` for both the cron file and the script."
            }
        ],
        "inspect_cmd": "ansible ubuntu,rhel -m command -a 'ls -la /etc/cron.d/malicious_beacon /opt/crypto_miner.sh /etc/security/audit_notice.txt'",
        # Playbook executed when learner enters or resets the scenario to plant the simulated outage
        "reset_playbook": (
            "---\n"
            "- name: Simulate Incident Condition (Plant Threat Artifacts)\n"
            "  hosts: ubuntu, rhel\n"
            "  gather_facts: false\n"
            "  tasks:\n"
            "    - name: Plant simulated rogue cron job\n"
            "      ansible.builtin.copy:\n"
            "        dest: /etc/cron.d/malicious_beacon\n"
            "        content: \"* * * * * root /opt/crypto_miner.sh >/dev/null 2>&1\\n\"\n"
            "        mode: '0644'\n\n"
            "    - name: Plant simulated rogue payload script\n"
            "      ansible.builtin.copy:\n"
            "        dest: /opt/crypto_miner.sh\n"
            "        content: \"#!/bin/sh\\necho beaconing\\n\"\n"
            "        mode: '0755'\n\n"
            "    - name: Clean slate audit notice\n"
            "      ansible.builtin.file:\n"
            "        path: /etc/security/audit_notice.txt\n"
            "        state: absent\n"
        ),
        # Playbook executed by the platform Verification Coach to test the learner's fix
        "validation_playbook": (
            "---\n"
            "- name: Validate Incident Remediation Across Fleet\n"
            "  hosts: ubuntu, rhel\n"
            "  gather_facts: false\n"
            "  tasks:\n"
            "    - name: Verify rogue cron is gone\n"
            "      ansible.builtin.stat:\n"
            "        path: /etc/cron.d/malicious_beacon\n"
            "      register: cron_stat\n"
            "      failed_when: cron_stat.stat.exists\n\n"
            "    - name: Verify payload script is gone\n"
            "      ansible.builtin.stat:\n"
            "        path: /opt/crypto_miner.sh\n"
            "      register: payload_stat\n"
            "      failed_when: payload_stat.stat.exists\n\n"
            "    - name: Verify audit notice exists and contains token\n"
            "      ansible.builtin.shell: |\n"
            "        test -f /etc/security/audit_notice.txt && grep -q 'INCIDENT_REMEDIATED=TRUE' /etc/security/audit_notice.txt\n"
            "      changed_when: false\n"
        ),
        "solution_type": "playbook",
        # Reference solution code shown in hints or upon passing
        "solution_code": (
            "---\n"
            "- name: P1 Incident Remediation — Purge Rogue Backdoors\n"
            "  hosts: ubuntu, rhel\n"
            "  gather_facts: false\n"
            "  tasks:\n"
            "    - name: 1. Purge unauthorized cron job persistence\n"
            "      ansible.builtin.file:\n"
            "        path: /etc/cron.d/malicious_beacon\n"
            "        state: absent\n\n"
            "    - name: 2. Remove malicious miner executable\n"
            "      ansible.builtin.file:\n"
            "        path: /opt/crypto_miner.sh\n"
            "        state: absent\n\n"
            "    - name: 3. Deploy tamper-evident security audit notice\n"
            "      ansible.builtin.copy:\n"
            "        dest: /etc/security/audit_notice.txt\n"
            "        content: \"INCIDENT_REMEDIATED=TRUE\\n\"\n"
            "        mode: '0644'\n"
        ),
        "explanation": (
            "### Incident Post-Mortem & Remediation Analysis\n\n"
            "1. **Persistence Neutralization**: Removing `/etc/cron.d/malicious_beacon` with `state: absent` halts recurring scheduled executions.\n"
            "2. **Binary Cleanup**: Removing `/opt/crypto_miner.sh` eliminates the executable artifact.\n"
            "3. **Compliance Token**: Writing `/etc/security/audit_notice.txt` satisfies SOC compliance verification."
        )
    }
]
```

Restart or start the lab with `./lab restart`, and your new track appears immediately in the lesson dropdown menu!

Pull requests, company incident packs, and community challenges are warmly welcome!

---

## 📄 License

Distributed under the **MIT License**. Free for personal learning, educational workshops, universities, and commercial teams.
