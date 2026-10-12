import os
import urllib.request
import urllib.parse
import json
import ssl
import time
import sys
import paramiko

PVE_HOST = os.getenv("PVE_HOST", "192.168.1.101")
PVE_USER = os.getenv("PVE_USER", "root@pam")
PVE_PASS = os.getenv("PVE_PASS", "change_me")
SSH_PUB_PATH = os.getenv("SSH_PUB_PATH", os.path.expanduser("~/.ssh/id_ed25519.pub"))

PUBKEY = ""
if os.path.exists(SSH_PUB_PATH):
    with open(SSH_PUB_PATH, "r") as f:
        PUBKEY = f.read().strip()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_pve_ticket():
    data = urllib.parse.urlencode({"username": PVE_USER, "password": PVE_PASS}).encode()
    req = urllib.request.Request(f"https://{PVE_HOST}:8006/api2/json/access/ticket", data=data)
    res = urllib.request.urlopen(req, context=ctx)
    auth = json.loads(res.read())
    return auth["data"]["ticket"], auth["data"]["CSRFPreventionToken"]

def wait_for_pve_task(ticket, upid, timeout=90):
    upid_q = urllib.parse.quote(upid)
    start = time.time()
    while time.time() - start < timeout:
        req = urllib.request.Request(f"https://{PVE_HOST}:8006/api2/json/nodes/pve/tasks/{upid_q}/status")
        req.add_header("Cookie", f"PVEAuthCookie={ticket}")
        res = urllib.request.urlopen(req, context=ctx)
        st = json.loads(res.read())["data"]
        if st.get("status") == "stopped":
            return st.get("exitstatus")
        time.sleep(2)
    return "TIMEOUT"

def get_existing_lxcs(ticket):
    req = urllib.request.Request(f"https://{PVE_HOST}:8006/api2/json/nodes/pve/lxc")
    req.add_header("Cookie", f"PVEAuthCookie={ticket}")
    res = urllib.request.urlopen(req, context=ctx)
    return {v["vmid"]: v for v in json.loads(res.read())["data"]}

nodes_to_create = [
    {
        "vmid": 302,
        "hostname": "node2-debian",
        "ostemplate": "local:vztmpl/debian-12-standard_12.12-1_amd64.tar.zst",
        "memory": 1024,
        "swap": 512,
        "cores": 1,
        "rootfs": "local-lvm:2.5",
        "net0": "name=eth0,bridge=vmbr0,ip=192.168.1.162/24,gw=192.168.1.1",
        "flavor": "debian"
    },
    {
        "vmid": 303,
        "hostname": "node3-debian13",
        "ostemplate": "local:vztmpl/debian-13-standard_13.6-1_amd64.tar.zst",
        "memory": 1024,
        "swap": 512,
        "cores": 1,
        "rootfs": "local-lvm:2.5",
        "net0": "name=eth0,bridge=vmbr0,ip=192.168.1.163/24,gw=192.168.1.1",
        "flavor": "debian"
    },
    {
        "vmid": 304,
        "hostname": "node4-almalinux",
        "ostemplate": "local:vztmpl/almalinux-9-default_20240911_amd64.tar.xz",
        "memory": 1024,
        "swap": 512,
        "cores": 1,
        "rootfs": "local-lvm:2.5",
        "net0": "name=eth0,bridge=vmbr0,ip=192.168.1.164/24,gw=192.168.1.1",
        "flavor": "rhel"
    },
    {
        "vmid": 305,
        "hostname": "node5-rocky",
        "ostemplate": "local:vztmpl/rockylinux-9-default_20240912_amd64.tar.xz",
        "memory": 1024,
        "swap": 512,
        "cores": 1,
        "rootfs": "local-lvm:2.5",
        "net0": "name=eth0,bridge=vmbr0,ip=192.168.1.165/24,gw=192.168.1.1",
        "flavor": "rhel"
    },
    {
        "vmid": 306,
        "hostname": "node6-alpine",
        "ostemplate": "local:vztmpl/alpine-3.22-default_20250617_amd64.tar.xz",
        "memory": 512,
        "swap": 256,
        "cores": 1,
        "rootfs": "local-lvm:1",
        "net0": "name=eth0,bridge=vmbr0,ip=192.168.1.166/24,gw=192.168.1.1",
        "flavor": "alpine"
    }
]

print("=== Starting Proxmox Cluster Provisioning ===")
ticket, csrf = get_pve_ticket()
existing = get_existing_lxcs(ticket)

for node in nodes_to_create:
    vmid = node["vmid"]
    if vmid in existing:
        print(f"[*] LXC {vmid} ({node['hostname']}) already exists.")
        continue

    print(f"[*] Creating LXC {vmid} ({node['hostname']}) using {node['ostemplate']}...")
    create_params = {
        "vmid": vmid,
        "ostemplate": node["ostemplate"],
        "hostname": node["hostname"],
        "memory": node["memory"],
        "swap": node["swap"],
        "cores": node["cores"],
        "rootfs": node["rootfs"],
        "net0": node["net0"],
        "nameserver": "1.1.1.1",
        "ssh-public-keys": PUBKEY,
        "password": PVE_PASS,
        "features": "nesting=1",
        "unprivileged": 1,
        "start": 1
    }

    req_c = urllib.request.Request(
        f"https://{PVE_HOST}:8006/api2/json/nodes/pve/lxc",
        data=urllib.parse.urlencode(create_params).encode()
    )
    req_c.add_header("Cookie", f"PVEAuthCookie={ticket}")
    req_c.add_header("CSRFPreventionToken", csrf)

    res = urllib.request.urlopen(req_c, context=ctx)
    upid = json.loads(res.read())["data"]
    status = wait_for_pve_task(ticket, upid)
    print(f"    Creation completed with status: {status}")

print("\n[*] Waiting 5 seconds for containers to initialize...")
time.sleep(5)

# Connect to Proxmox host via SSH to configure services inside containers
print("[*] Connecting to Proxmox host via SSH to configure services inside containers...")
pve_ssh = paramiko.SSHClient()
pve_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
pve_ssh.connect(PVE_HOST, username="root", password=PVE_PASS, look_for_keys=False, allow_agent=False)

all_nodes = [
    {"vmid": 301, "flavor": "ubuntu", "name": "node1-ubuntu"},
    {"vmid": 302, "flavor": "debian", "name": "node2-debian"},
    {"vmid": 303, "flavor": "debian", "name": "node3-debian13"},
    {"vmid": 304, "flavor": "rhel", "name": "node4-almalinux"},
    {"vmid": 305, "flavor": "rhel", "name": "node5-rocky"},
    {"vmid": 306, "flavor": "alpine", "name": "node6-alpine"}
]

for n in all_nodes:
    vmid = n["vmid"]
    flavor = n["flavor"]
    print(f"[*] Configuring guest services on {n['name']} (VMID {vmid})...")
    
    if flavor in ["ubuntu", "debian"]:
        script = f"""
pct exec {vmid} -- ssh-keygen -A 2>/dev/null || true
pct exec {vmid} -- systemctl enable --now ssh 2>/dev/null || pct exec {vmid} -- service ssh restart 2>/dev/null || true
"""
    elif flavor == "rhel":
        script = f"""
pct exec {vmid} -- ssh-keygen -A 2>/dev/null || true
pct exec {vmid} -- systemctl enable --now sshd 2>/dev/null || true
"""
    elif flavor == "alpine":
        script = f"""
pct exec {vmid} -- apk update
pct exec {vmid} -- apk add python3 openssh-server bash
pct exec {vmid} -- ssh-keygen -A
pct exec {vmid} -- rc-update add sshd default
pct exec {vmid} -- rc-service sshd restart
pct exec {vmid} -- mkdir -p /root/.ssh
pct exec {vmid} -- sh -c 'echo "{PUBKEY}" > /root/.ssh/authorized_keys'
pct exec {vmid} -- chmod 700 /root/.ssh
pct exec {vmid} -- chmod 600 /root/.ssh/authorized_keys
"""
    _, stdout, stderr = pve_ssh.exec_command(script)
    stdout.channel.recv_exit_status()
    print(f"    Guest {n['name']} configuration done.")

pve_ssh.close()
print("=== All nodes provisioned and configured successfully! ===")
