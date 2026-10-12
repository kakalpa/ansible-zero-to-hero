FROM alpine:3.22

RUN apk add --no-cache \
    openssh \
    openssh-server \
    python3 \
    sudo \
    curl \
    iputils \
    bash \
    procps

RUN mkdir -p /var/run/sshd /root/.ssh && \
    chmod 700 /root/.ssh && \
    ssh-keygen -A

COPY docker/keys/id_ed25519.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

COPY docker/node-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
