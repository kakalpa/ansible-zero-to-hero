import os
import subprocess
import json

PROJECT_DIR = os.getenv("PROJECT_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def inspect_node_state(command_str: str, target: str = "all"):
    """Run an ad-hoc command to inspect target state on remote nodes"""
    cmd = f"ansible {target} -m shell -a \"{command_str}\""
    env = os.environ.copy()
    env["ANSIBLE_LOG_PATH"] = "/dev/null"
    res = subprocess.run(cmd, shell=True, env=env, cwd=PROJECT_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=20)
    return res.stdout

