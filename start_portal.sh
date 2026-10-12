#!/usr/bin/env bash
cd "$(dirname "$0")/ansible_lab_portal"
echo "Starting Ansible Zero-to-Hero Lab Portal on http://localhost:8080 ..."
exec python3 -m uvicorn app:app --host 0.0.0.0 --port 8080 --reload
