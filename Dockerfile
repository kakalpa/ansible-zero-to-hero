FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PROJECT_DIR=/ansible

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    iputils-ping \
    curl \
    git \
    bash \
    procps \
    ca-certificates \
    nano \
    vim \
    neovim \
    less \
    && rm -rf /var/lib/apt/lists/*

COPY config/vimrc /etc/vim/vimrc.local
RUN cp /etc/vim/vimrc.local /root/.vimrc && \
    mkdir -p /etc/xdg/nvim /root/.config/nvim && \
    cp /etc/vim/vimrc.local /etc/xdg/nvim/sysinit.vim && \
    cp /etc/vim/vimrc.local /root/.config/nvim/init.vim

COPY config/nanorc /etc/nanorc
RUN cp /etc/nanorc /root/.nanorc

WORKDIR /ansible

COPY requirements.txt /ansible/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN ansible-galaxy collection install community.general ansible.posix

COPY ansible.cfg inventory.ini inventory.yaml playbook.yaml /ansible/
COPY playbooks/ /ansible/playbooks/
COPY ansible_lab_portal/ /ansible/ansible_lab_portal/
COPY docker/ /ansible/docker/
RUN ln -sf inventory.ini hosts

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["python3", "-m", "uvicorn", "ansible_lab_portal.app:app", "--host", "0.0.0.0", "--port", "8080"]
