#!/bin/sh
set -e

mkdir -p /var/run/sshd /run/openrc
touch /run/openrc/softlevel
ssh-keygen -A 2>/dev/null || true

# Pre-configure default site config for nginx on Alpine
if [ ! -f /etc/nginx/http.d/default.conf ]; then
    mkdir -p /etc/nginx/http.d
    cat << 'EOFNGINX' > /etc/nginx/http.d/default.conf
server {
    listen 80 default_server;
    root /var/lib/nginx/html;
    index index.html;
}
EOFNGINX
fi

# If dynamic key is provided via shared volume, sync it
if [ -f /shared-keys/id_ed25519.pub ]; then
    cat /shared-keys/id_ed25519.pub >> /root/.ssh/authorized_keys
    sort -u /root/.ssh/authorized_keys -o /root/.ssh/authorized_keys
fi

if [ -f /root/.ssh/authorized_keys ]; then
    chmod 600 /root/.ssh/authorized_keys
fi

exec /usr/sbin/sshd -D -e
