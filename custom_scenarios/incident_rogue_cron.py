# ==============================================================================
#  Custom Scenario Example: P1 Incident Response & Fleet Backdoor Remediation
#  Place any *.py scenario files in custom_scenarios/ to automatically load them!
# ==============================================================================

CUSTOM_MODULE = {
    "id": "incidents",
    "title": "Incident Response: SRE War Room Scenarios",
    "desc": "Real-world production outages, security incidents, and cascading failures to diagnose and remediate.",
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
            "The DataForge Security Operations Center (SOC) detected unauthorized outbound beaconing "
            "and abnormal CPU spikes across both `node1-ubuntu` and `node4-almalinux`.\n\n"
            "Initial forensics discovered a supply-chain attack: an attacker dropped an unauthorized cron job at "
            "`/etc/cron.d/malicious_beacon` which attempts to launch `/opt/crypto_miner.sh` every minute.\n\n"
            "**Incident Commander Instructions:**\n"
            "> *\"Author an idempotent remediation playbook at `/ansible/remediate_incident.yml`. "
            "Safely purge the cron persistence file, remove the malicious script, and deploy a hardened "
            "audit banner to `/etc/security/audit_notice.txt` confirming incident containment.\"*"
        ),
        "tasks": [
            "1. Target both affected node groups (`ubuntu` and `rhel`).",
            "2. Ensure `/etc/cron.d/malicious_beacon` is permanently deleted (`state: absent`).",
            "3. Ensure `/opt/crypto_miner.sh` is permanently removed (`state: absent`).",
            "4. Deploy `/etc/security/audit_notice.txt` containing 'INCIDENT_REMEDIATED=TRUE' with permissions 0644."
        ],
        "primer": {
            "concept": (
                "Incident response in fleet orchestration requires idempotent cleanup. Using `ansible.builtin.file` "
                "with `state: absent` ensures that malicious artifacts are eradicated without failing if a node was already sanitized."
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
                "    - name: Enforce security audit compliance token\n"
                "      ansible.builtin.copy:\n"
                "        dest: /etc/security/audit_token\n"
                "        content: \"AUDIT_VERIFIED=TRUE\\n\"\n"
                "        mode: '0644'\n"
            ),
            "quick_tip": "Always set `state: absent` rather than executing `rm -f`. The file module is safe, idempotent, and cross-platform.",
            "syntax_breakdown": [
                {"element": "hosts: ubuntu, rhel", "role": "Targets both the Debian-family and RHEL-family affected nodes simultaneously"},
                {"element": "state: absent", "role": "Idempotently deletes the target file or directory if it exists"},
                {"element": "mode: '0644'", "role": "Enforces secure POSIX permissions on newly deployed compliance artifacts"}
            ]
        },
        "hints": [
            {
                "level": "Hint 1: Targeting Multiple Groups",
                "text": "In your playbook header, specify multiple groups separated by a comma or colon: `hosts: ubuntu, rhel`."
            },
            {
                "level": "Hint 2: Idempotent File Deletion",
                "text": "Use the `ansible.builtin.file` module with `path: /etc/cron.d/malicious_beacon` and `state: absent`."
            },
            {
                "level": "Hint 3: Playbook Structure",
                "text": "Create tasks for: 1. Removing /etc/cron.d/malicious_beacon, 2. Removing /opt/crypto_miner.sh, 3. Copying /etc/security/audit_notice.txt with content 'INCIDENT_REMEDIATED=TRUE\\n'."
            }
        ],
        "inspect_cmd": "ansible ubuntu,rhel -m command -a 'ls -la /etc/cron.d/malicious_beacon /opt/crypto_miner.sh /etc/security/audit_notice.txt'",
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
            "        content: \"#!/bin/sh\\n# Rogue Beacon Simulator\\necho beaconing\\n\"\n"
            "        mode: '0755'\n\n"
            "    - name: Ensure clean audit notice slate\n"
            "      ansible.builtin.file:\n"
            "        path: /etc/security/audit_notice.txt\n"
            "        state: absent\n"
        ),
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
            "1. **Persistence Neutralization**: Removing `/etc/cron.d/malicious_beacon` with `state: absent` stops the cron daemon from triggering recurring attacks.\n"
            "2. **Binary Cleanup**: Removing `/opt/crypto_miner.sh` eliminates the payload.\n"
            "3. **Compliance Token**: Writing `/etc/security/audit_notice.txt` with `mode: '0644'` provides deterministic proof for the SOC audit crawler that the node is remediated."
        )
    }
]
