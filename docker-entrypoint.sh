#!/bin/bash
set -e

mkdir -p /root/.ssh
chmod 700 /root/.ssh

KEY_SOURCE="/ansible/docker/keys"
if [ -d /shared-keys ]; then
    KEY_SOURCE="/shared-keys"
fi
mkdir -p "$KEY_SOURCE"

if [ ! -f "$KEY_SOURCE/id_ed25519" ]; then
    echo "[*] Generating fresh Ed25519 cluster keypair..."
    ssh-keygen -t ed25519 -N "" -C "ansible-portal@cluster" -f "$KEY_SOURCE/id_ed25519"
    chmod 600 "$KEY_SOURCE/id_ed25519"
    chmod 644 "$KEY_SOURCE/id_ed25519.pub"
fi

cp "$KEY_SOURCE/id_ed25519" /root/.ssh/master
cp "$KEY_SOURCE/id_ed25519" /root/.ssh/id_ed25519
chmod 600 /root/.ssh/master /root/.ssh/id_ed25519

if [ -d /shared-keys ] && [ "$KEY_SOURCE" != "/shared-keys" ]; then
    cp "$KEY_SOURCE/id_ed25519.pub" /shared-keys/id_ed25519.pub 2>/dev/null || true
fi

cat <<'EOFCONFIG' > /root/.ssh/config
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
EOFCONFIG
chmod 600 /root/.ssh/config

echo "[*] Initializing Ansible Zero-to-Hero Portal..."
echo "[*] Working directory: $(pwd)"

# Ensure less pager is installed
if ! command -v less >/dev/null 2>&1; then
    apt-get update -qq && apt-get install -y -qq less >/dev/null 2>&1 || true
fi

# Configure clean pager defaults for interactive Ansible documentation browsing
export PAGER="less -R -F -X"
export LESS="-R -F -X"
grep -q "PAGER=" /etc/environment 2>/dev/null || echo 'PAGER="less -R -F -X"' >> /etc/environment
grep -q "LESS=" /etc/environment 2>/dev/null || echo 'LESS="-R -F -X"' >> /etc/environment

# Ensure ansible-doc audit logging wrapper is active
if [ -f /usr/local/bin/ansible-doc ] && [ ! -f /usr/local/bin/ansible-doc.orig ]; then
    cp /usr/local/bin/ansible-doc /usr/local/bin/ansible-doc.orig
    cat << 'EOFWRAP' > /usr/local/bin/ansible-doc
#!/bin/bash
if [ "$ANSIBLE_LOG_PATH" != "/dev/null" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') localhost ansible-doc: $*" >> /var/log/ansible.log 2>/dev/null || true
fi
exec /usr/local/bin/ansible-doc.orig "$@"
EOFWRAP
    chmod +x /usr/local/bin/ansible-doc
fi

exec "$@"
