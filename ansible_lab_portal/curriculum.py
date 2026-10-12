import os
import sys
import importlib.util

try:
    from .curriculum_levels import (
        LEVEL1_EXERCISES,
        LEVEL2_EXERCISES,
        LEVEL3_EXERCISES,
        LEVEL4_EXERCISES
    )
except ImportError:
    from curriculum_levels import (
        LEVEL1_EXERCISES,
        LEVEL2_EXERCISES,
        LEVEL3_EXERCISES,
        LEVEL4_EXERCISES
    )

MODULES = [
    {
        "id": "lvl1",
        "title": "Level 1: Fleet Discovery & Ad-Hoc Recon",
        "desc": "Join DataForge, explore inventory slices, inspect hardware, query facts, and master ad-hoc commands.",
        "badge": "Fleet Scout",
        "xp_per_lesson": 50
    },
    {
        "id": "lvl2",
        "title": "Level 2: Automation Blueprint — Declarative Playbooks",
        "desc": "Formalize operations into repeatable YAML playbooks, manage users, SSH keys, files, and check mode.",
        "badge": "YAML Sculptor",
        "xp_per_lesson": 100
    },
    {
        "id": "lvl3",
        "title": "Level 3: Dynamic Logic — Variables, Facts, Loops & Conditionals",
        "desc": "Build adaptable multi-distro automation with variables, loops, facts, when conditions, and assertions.",
        "badge": "Polyglot Systems",
        "xp_per_lesson": 150
    },
    {
        "id": "lvl4",
        "title": "Level 4: Production Engineering — Templates, Handlers & Resilience",
        "desc": "Master Jinja2 templating, event-driven handlers, modular roles, fault tolerance, and zero-downtime rolling waves.",
        "badge": "Principal Hero",
        "xp_per_lesson": 200
    }
]

EXERCISES = LEVEL1_EXERCISES + LEVEL2_EXERCISES + LEVEL3_EXERCISES + LEVEL4_EXERCISES

DEFAULT_TARGET_FILES = {
    # Level 2 (17 lessons)
    "l2-1-first-playbook": "/ansible/ping.yml",
    "l2-2-debug-module": "/ansible/debug_msg.yml",
    "l2-3-motd-banner": "/ansible/motd.yml",
    "l2-4-lineinfile-hosts": "/ansible/hosts.yml",
    "l2-5-blockinfile": "/ansible/block_config.yml",
    "l2-6-directory-scaffolding": "/ansible/directories.yml",
    "l2-7-user-management": "/ansible/users.yml",
    "l2-8-privilege-delegation": "/ansible/privilege_mgmt.yml",
    "l2-9-ssh-provisioning": "/ansible/ssh_keys.yml",
    "l2-10-software-provisioning": "/ansible/install_software.yml",
    "l2-11-service-control": "/ansible/services.yml",
    "l2-12-multi-task-play": "/ansible/app_config.yml",
    "l2-13-permissions-hardening": "/ansible/permissions.yml",
    "l2-14-purge-deprecated": "/ansible/vault.yml",
    "l2-15-dry-run-check": "/ansible/compliance.yml",
    "l2-16-host-onboarding": "/ansible/onboard_client.yml",
    "l2-17-level2-capstone": "/ansible/fleet_baseline.yml",
    # Level 3 (13 lessons)
    "l3-1-vars-section": "/ansible/vars.yml",
    "l3-2-vars-files": "/ansible/site_vars.yml",
    "l3-3-loop-lists": "/ansible/loop_lists.yml",
    "l3-4-loop-dicts": "/ansible/loop_dicts.yml",
    "l3-5-facts-in-playbooks": "/ansible/facts.yml",
    "l3-6-conditionals-when": "/ansible/conditionals.yml",
    "l3-7-package-module": "/ansible/generic_package.yml",
    "l3-8-multi-distro-packages": "/ansible/packages.yml",
    "l3-9-register-output": "/ansible/kernel.yml",
    "l3-10-reactive-when": "/ansible/reactive.yml",
    "l3-11-changed-when": "/ansible/uptime.yml",
    "l3-12-assert-validation": "/ansible/polyglot_fix.yml",
    "l3-13-level3-capstone": "/ansible/fleet_matrix.yml",
    # Level 4 (14 lessons)
    "l4-1-handlers-notify": "/ansible/handlers.yml",
    "l4-2-flush-handlers": "/ansible/flush.yml",
    "l4-3-jinja2-templates": "/ansible/template.yml",
    "l4-4-jinja2-filters": "/ansible/filters.yml",
    "l4-5-dynamic-hosts-template": "/ansible/inventory_hosts.yml",
    "l4-6-modular-tasks": "/ansible/site.yml",
    "l4-7-tags-execution": "/ansible/tagged_tasks.yml",
    "l4-8-role-scaffolding": "/ansible/roles_scaffold.yml",
    "l4-9-role-execution": "/ansible/roles_site.yml",
    "l4-10-ansible-vault": "/ansible/vault_secret.yml",
    "l4-11-fault-tolerance": "/ansible/rescue.yml",
    "l4-12-rolling-updates": "/ansible/rolling.yml",
    "l4-13-capstone-launch": "/ansible/canary_deploy.yml",
    "l4-14-grand-capstone": "/ansible/provision_client.yml",
}

# Dynamically load any custom scenario packs placed in custom_scenarios/
_custom_dirs = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "custom_scenarios"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_scenarios")
]
for _cdir in _custom_dirs:
    if os.path.isdir(_cdir):
        for _fname in sorted(os.listdir(_cdir)):
            if _fname.endswith(".py") and not _fname.startswith("__"):
                try:
                    _fpath = os.path.join(_cdir, _fname)
                    _mod_name = f"custom_scenario_{_fname[:-3]}"
                    _spec = importlib.util.spec_from_file_location(_mod_name, _fpath)
                    if _spec and _spec.loader:
                        _mod = importlib.util.module_from_spec(_spec)
                        _spec.loader.exec_module(_mod)
                        if hasattr(_mod, "CUSTOM_MODULE"):
                            if _mod.CUSTOM_MODULE["id"] not in [m["id"] for m in MODULES]:
                                MODULES.append(_mod.CUSTOM_MODULE)
                        if hasattr(_mod, "CUSTOM_EXERCISES"):
                            for _cex in _mod.CUSTOM_EXERCISES:
                                if _cex["id"] not in [e["id"] for e in EXERCISES]:
                                    EXERCISES.append(_cex)
                                    if "target_file" in _cex:
                                        DEFAULT_TARGET_FILES[_cex["id"]] = _cex["target_file"]
                except Exception as _e:
                    print(f"[!] Warning: Failed loading custom scenario {_fname}: {_e}")

for ex in EXERCISES:
    if ex["id"] in DEFAULT_TARGET_FILES and not ex.get("target_file"):
        ex["target_file"] = DEFAULT_TARGET_FILES[ex["id"]]
