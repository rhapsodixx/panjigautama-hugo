# VPS Compose + Caddy Deploy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the Hugo blog for sumopod VPS deploy on Docker network `web`, with a local deploy script and GitHub Action that SSH in and rebuild from git (no registry).

**Architecture:** Change Compose to join external `web` and drop host ports. Add `scripts/deploy.sh` that SSHs to the VPS and runs pull + submodule + `compose build/up`. Add `.github/workflows/deploy.yml` on push to `main` using the same remote commands and SSH deploy-key secrets. Docs already describe cutover; this plan only adjusts any leftover localhost-port references for Compose verification.

**Tech Stack:** Docker Compose, bash, GitHub Actions (`appleboy/ssh-action`), host Caddy on `web`, Hugo multi-stage Dockerfile (unchanged)

## Global Constraints

- Install path on VPS: `/opt/panjigautama-hugo`
- External Docker network name: `web`
- Container name: `panjigautama-hugo`
- In-container listen port: `8080`
- Host Caddy upstream: `panjigautama-hugo:8080` (no `127.0.0.1` publish)
- No Docker Hub / GHCR image push
- SSH auth only (ed25519 deploy key); never commit private keys or passwords
- VPS host (documented): `103.92.215.36`; GitHub secrets supply actual host/user/path
- Spec: `docs/superpowers/specs/2026-07-31-vps-compose-caddy-deploy-design.md`
- ADR: `docs/decisions/ADR-004-compose-build-host-caddy.md`

---

## File map

| File | Responsibility |
|------|----------------|
| `docker-compose.yml` | Blog service on external `web`; no host ports |
| `scripts/deploy.sh` | Local/CI-friendly SSH deploy: pull, submodules, compose rebuild |
| `.github/workflows/deploy.yml` | On push to `main`, SSH and run the same remote deploy commands |
| `docs/qa-checklist.md` | Note how to verify Compose via network `web` (optional appendix; do not rewrite historical Pass results) |
| `Caddyfile.snippet` / ADR / cutover | Already updated in docs commit — do not re-litigate |

**Unchanged:** `Dockerfile`, `docker/Caddyfile.container`, Hugo site content.

---

### Task 1: Compose on external network `web`

**Files:**
- Modify: `docker-compose.yml`
- Test: local Docker (create `web` if missing, build, curl via network)

**Interfaces:**
- Consumes: existing `Dockerfile` exposing `8080`; `container_name: panjigautama-hugo`
- Produces: Compose service reachable only as `http://panjigautama-hugo:8080` on network `web`

- [ ] **Step 1: Replace `docker-compose.yml` contents**

```yaml
services:
  blog:
    build: .
    container_name: panjigautama-hugo
    restart: unless-stopped
    networks:
      - web

networks:
  web:
    external: true
```

- [ ] **Step 2: Ensure network `web` exists and build**

Run:

```bash
docker network ls | grep -w web || docker network create web
docker compose build && docker compose up -d
docker compose ps
```

Expected: `blog` / `panjigautama-hugo` state `running` (or `Up`); no `0.0.0.0:8080` or `127.0.0.1:8080` in Ports column (Ports empty or only internal).

- [ ] **Step 3: Smoke-test via network `web`**

Run:

```bash
docker run --rm --network web curlimages/curl:8.5.0 -sI http://panjigautama-hugo:8080/ | head -1
docker run --rm --network web curlimages/curl:8.5.0 -s -o /dev/null -w "%{http_code}\n" http://panjigautama-hugo:8080/about-me/
```

Expected: first line `HTTP/1.1 200 OK` (or `HTTP/2 200`); second line `200`.

If Docker daemon is unavailable, skip runtime steps, still commit the YAML, and note the skip in the PR/commit body.

- [ ] **Step 4: Commit**

```bash
git add docker-compose.yml
git commit -m "$(cat <<'EOF'
fix: join Docker network web without publishing host ports

Match sumopod Caddy peers (Vaultwarden-style) per ADR-004.
EOF
)"
```

---

### Task 2: Local deploy script

**Files:**
- Create: `scripts/deploy.sh`
- Test: bash syntax + dry-run / missing-env failure (no live VPS required)

**Interfaces:**
- Consumes: env `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY` **or** `SSH_KEY_FILE`, optional `DEPLOY_PATH` (default `/opt/panjigautama-hugo`)
- Produces: exit `0` after successful remote rebuild; prints clear errors if env missing

- [ ] **Step 1: Write failing check for missing env**

Create `scripts/deploy.sh` as a stub that always exits 0 (will replace in Step 3), then run the missing-env test against the **real** script after Step 3. Prefer writing the full script in Step 3 and verifying failure modes there.

Create the full script in the next step; first add an executable placeholder only if needed for TDD ordering. Preferred path: write the complete script below, then run negative tests.

- [ ] **Step 2: Write `scripts/deploy.sh`**

```bash
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
```

- [ ] **Step 3: Make executable and verify negative cases**

Run:

```bash
chmod +x scripts/deploy.sh
bash -n scripts/deploy.sh
( unset SSH_HOST SSH_USER SSH_KEY_FILE SSH_PRIVATE_KEY; ./scripts/deploy.sh ) ; echo "exit=$?"
```

Expected: `bash -n` silent (syntax OK). Second command prints `error: SSH_HOST and SSH_USER are required` and `exit=1`.

Run:

```bash
SSH_HOST=127.0.0.1 SSH_USER=root ./scripts/deploy.sh ; echo "exit=$?"
```

Expected: `error: set SSH_KEY_FILE or SSH_PRIVATE_KEY` and `exit=1`.

- [ ] **Step 4: Commit**

```bash
git add scripts/deploy.sh
git commit -m "$(cat <<'EOF'
feat: add SSH deploy script for VPS git rebuild

Pull, update submodules, and compose build/up on the remote host.
EOF
)"
```

---

### Task 3: GitHub Action deploy workflow

**Files:**
- Create: `.github/workflows/deploy.yml`

**Interfaces:**
- Consumes: GitHub secrets `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`, `DEPLOY_PATH`
- Produces: on push to `main`, remote runs the same pull/submodule/compose sequence as `scripts/deploy.sh`

- [ ] **Step 1: Create `.github/workflows/deploy.yml`**

```yaml
name: Deploy to VPS

on:
  push:
    branches:
      - main
  workflow_dispatch:

concurrency:
  group: deploy-vps
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy over SSH
        uses: appleboy/ssh-action@v1.2.0
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script_stop: true
          script: |
            set -euo pipefail
            cd "${{ secrets.DEPLOY_PATH }}"
            git pull
            git submodule update --init --recursive
            docker compose build && docker compose up -d
            docker compose ps
```

Note: `DEPLOY_PATH` must be set as a repository secret (value `/opt/panjigautama-hugo`). Do not hardcode the VPS IP in the workflow; use `SSH_HOST`.

- [ ] **Step 2: Validate workflow YAML**

Run (if `actionlint` is installed):

```bash
actionlint .github/workflows/deploy.yml
```

Expected: no errors. If `actionlint` is missing, validate structure manually: `on.push.branches` includes `main`; secrets referenced as above; `script_stop: true`.

Alternatively:

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml')); print('yaml ok')"
```

Expected: `yaml ok` (requires PyYAML). If unavailable, skip and rely on GitHub’s workflow editor after push.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/deploy.yml
git commit -m "$(cat <<'EOF'
ci: deploy to VPS on push to main via SSH

Rebuild the Compose blog from git using deploy-key secrets.
EOF
)"
```

- [ ] **Step 4: Document operator secret setup (no commit of secrets)**

Remind in the PR or handoff notes (do not put private keys in the repo):

```text
GitHub → Settings → Secrets and variables → Actions:
  SSH_HOST=103.92.215.36
  SSH_USER=root
  SSH_PRIVATE_KEY=<contents of panjigautama-hugo-deploy>
  DEPLOY_PATH=/opt/panjigautama-hugo
```

First VPS clone must exist before the Action can `cd` and `git pull` (see cutover runbook). Until secrets are set, use `workflow_dispatch` only after secrets exist, or rely on `scripts/deploy.sh`.

---

### Task 4: QA checklist Compose note + CLAUDE deploy pointer

**Files:**
- Modify: `docs/qa-checklist.md` (append section only)
- Modify: `CLAUDE.md` only if the Stack/Deploy rows are missing the script/Action (already updated — verify; skip if accurate)

**Interfaces:**
- Consumes: Task 1 Compose networking
- Produces: Future agents know not to curl `127.0.0.1:8080` for Compose on `web`

- [ ] **Step 1: Append to `docs/qa-checklist.md`**

Add at the end of the file (exact content):

```markdown
## Compose verification (network `web`)

After ADR-004 revision, Compose does **not** publish `127.0.0.1:8080`. Verify with:

```bash
docker network ls | grep -w web || docker network create web
docker compose build && docker compose up -d
docker run --rm --network web curlimages/curl:8.5.0 -sI http://panjigautama-hugo:8080/ | head -1
```

Historical checks above used Hugo `public/` + `python3 -m http.server` or an older Compose port publish; those results remain valid for content QA.
```

- [ ] **Step 2: Verify `CLAUDE.md` Deploy / Edge rows mention git rebuild and `web`**

If already present from the docs commit, make no change. If stale, align with ADR-004 one-liners.

- [ ] **Step 3: Commit**

```bash
git add docs/qa-checklist.md CLAUDE.md
git commit -m "$(cat <<'EOF'
docs: note Compose smoke checks via Docker network web

Avoid implying host port 8080 after the ADR-004 networking change.
EOF
)"
```

---

### Task 5: End-to-end dry validation (local)

**Files:**
- None (verification only)

**Interfaces:**
- Consumes: Tasks 1–3 artifacts

- [ ] **Step 1: Confirm repo artifacts exist**

Run:

```bash
test -f docker-compose.yml && grep -q 'external: true' docker-compose.yml
test -x scripts/deploy.sh && bash -n scripts/deploy.sh
test -f .github/workflows/deploy.yml && grep -q 'appleboy/ssh-action' .github/workflows/deploy.yml
grep -q 'panjigautama-hugo:8080' Caddyfile.snippet
```

Expected: all commands exit 0.

- [ ] **Step 2: Optional live Compose rebuild**

Same as Task 1 Steps 2–3 if Docker is available.

- [ ] **Step 3: No commit unless fixes were needed**

If any check failed, fix in the owning task’s files and amend only per project git rules (prefer a new fix commit).

---

## Spec coverage (self-review)

| Spec requirement | Task |
|------------------|------|
| Compose on `web`, no host ports | Task 1 |
| Caddy upstream by container name | Already in `Caddyfile.snippet` / docs; verified Task 5 |
| No Docker Hub | Global constraint; no registry steps |
| `scripts/deploy.sh` | Task 2 |
| GitHub Action on `main` | Task 3 |
| SSH deploy key (docs / secrets) | Task 3 Step 4 + existing cutover §0 |
| Content = git pull + rebuild | Tasks 2–3 remote commands |
| First-install Ubuntu steps | Already in `docs/operations-cutover.md` (ops, not code) |
| QA curl via `web` | Tasks 1, 4 |

## Out of scope for this plan

- Actually SSHing to `103.92.215.36` or setting GitHub secrets (operator)
- WordPress cutover / Caddy reload on production
- Generating the deploy key in CI
- Changing Hugo content or Dockerfile

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-31-vps-compose-caddy-deploy.md`. Two execution options:

**1. Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
