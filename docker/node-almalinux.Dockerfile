FROM almalinux:9

RUN dnf install -y --setopt=install_weak_deps=False --allowerasing \
    openssh-server \
    python3 \
    sudo \
    iputils \
    procps-ng \
    && dnf clean all

RUN mkdir -p /var/run/sshd /root/.ssh && \
    chmod 700 /root/.ssh && \
    ssh-keygen -A

COPY docker/keys/id_ed25519.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

COPY docker/node-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
