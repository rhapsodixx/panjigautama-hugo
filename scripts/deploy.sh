#!/usr/bin/env bash
# Deploy panjigautama-hugo to the VPS: git pull + submodule + compose rebuild.
# Required env: SSH_HOST, SSH_USER
# Auth: SSH_KEY_FILE (path) or SSH_PRIVATE_KEY (PEM contents)
# Optional: DEPLOY_PATH (default /opt/panjigautama-hugo)
set -euo pipefail

DEPLOY_PATH="${DEPLOY_PATH:-/opt/panjigautama-hugo}"

if [[ -z "${SSH_HOST:-}" || -z "${SSH_USER:-}" ]]; then
  echo "error: SSH_HOST and SSH_USER are required" >&2
  exit 1
fi

TMP_KEY=""
cleanup() {
  if [[ -n "${TMP_KEY}" && -f "${TMP_KEY}" ]]; then
    rm -f "${TMP_KEY}"
  fi
}
trap cleanup EXIT

SSH_OPTS=(-o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new)

if [[ -n "${SSH_KEY_FILE:-}" ]]; then
  if [[ ! -f "${SSH_KEY_FILE}" ]]; then
    echo "error: SSH_KEY_FILE not found: ${SSH_KEY_FILE}" >&2
    exit 1
  fi
  SSH_OPTS+=(-i "${SSH_KEY_FILE}")
elif [[ -n "${SSH_PRIVATE_KEY:-}" ]]; then
  TMP_KEY="$(mktemp)"
  chmod 600 "${TMP_KEY}"
  printf '%s\n' "${SSH_PRIVATE_KEY}" > "${TMP_KEY}"
  SSH_OPTS+=(-i "${TMP_KEY}")
else
  echo "error: set SSH_KEY_FILE or SSH_PRIVATE_KEY" >&2
  exit 1
fi

REMOTE_CMD=$(cat <<EOF
set -euo pipefail
cd "${DEPLOY_PATH}"
git pull
git submodule update --init --recursive
docker compose build && docker compose up -d
docker compose ps
EOF
)

echo "Deploying to ${SSH_USER}@${SSH_HOST}:${DEPLOY_PATH}"
ssh "${SSH_OPTS[@]}" "${SSH_USER}@${SSH_HOST}" "${REMOTE_CMD}"
echo "Deploy finished."
