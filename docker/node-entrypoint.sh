#!/bin/sh
set -e

mkdir -p /var/run/sshd
ssh-keygen -A 2>/dev/null || true

# If dynamic key is provided via shared volume, sync it
if [ -f /shared-keys/id_ed25519.pub ]; then
    cat /shared-keys/id_ed25519.pub >> /root/.ssh/authorized_keys
    sort -u /root/.ssh/authorized_keys -o /root/.ssh/authorized_keys
fi

if [ -f /root/.ssh/authorized_keys ]; then
    chmod 600 /root/.ssh/authorized_keys
fi

exec /usr/sbin/sshd -D -e
