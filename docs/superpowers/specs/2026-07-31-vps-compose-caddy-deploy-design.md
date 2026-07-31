# VPS Deploy Design — Compose on `web` + host Caddy + git deploy

**Date:** 2026-07-31  
**Status:** Approved (pending implementation plan)  
**Host:** sumopod VPS `103.92.215.36` (Ubuntu)  
**Related:** [ADR-004](../../decisions/ADR-004-compose-build-host-caddy.md), [ADR-005](../../decisions/ADR-005-multi-domain-aliases.md), [`docs/operations-cutover.md`](../../operations-cutover.md)

## Goal

Deploy the Hugo blog on the existing sumopod VPS beside other Compose apps (e.g. Vaultwarden), behind host Caddy on Docker network `web`. Ship content via git; rebuild on the VPS. Automate with a local script and a GitHub Action. No Docker Hub.

## Decisions

| Topic | Choice |
|-------|--------|
| Install path | `/opt/panjigautama-hugo` |
| Image source | Build on VPS from git (`docker compose build`) — no registry |
| Docker network | External `web`; no host port publish |
| Caddy upstream | `reverse_proxy panjigautama-hugo:8080` (container name) |
| Content workflow | Edit Markdown locally → push `main` → deploy pulls + rebuilds |
| Automation | Both: `scripts/deploy.sh` and GitHub Action on push to `main` |
| Auth to VPS | SSH ed25519 deploy key (not root password in CI) |
| Domains | Unchanged — ADR-005 |

**Assumption:** Host Caddy runs as a Docker container attached to network `web` (same pattern as Vaultwarden’s `reverse_proxy vaultwarden:80`). If Caddy were host-only systemd, this design would need a localhost port publish instead.

## Architecture

```text
Laptop / GitHub Actions
        │ SSH (deploy key)
        ▼
/opt/panjigautama-hugo   (git clone)
        │ docker compose build && up -d
        ▼
container panjigautama-hugo :8080  ──network web──►  Caddy (TLS)
                                                      │
                                                      ▼
                         panjigautama.com / www / blog.kamisamanosumopod.my.id
```

### Compose shape (target)

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

No `ports:` mapping. In-container Caddy still listens on `8080` (`docker/Caddyfile.container`).

### Host Caddy site block

```caddy
panjigautama.com, www.panjigautama.com, blog.kamisamanosumopod.my.id {
	encode gzip
	reverse_proxy panjigautama-hugo:8080
}
```

## Out of scope

- Pushing images to Docker Hub / GHCR
- Password-based GitHub Actions SSH
- Automated WordPress teardown
- Staging subdomain

## New / edited posts

1. Author Markdown under `site/content/` locally; optional `hugo server` QA.
2. Commit and push to `main` on GitHub.
3. Deploy (Action or `./scripts/deploy.sh`) on the VPS:
   - `git pull`
   - `git submodule update --init --recursive`
   - `docker compose build && docker compose up -d`
4. Smoke-check homepage over HTTPS.

No CMS; the git repo is the source of truth.

## SSH deploy key (Ubuntu VPS)

Generate on a trusted machine (not committed to the repo):

```bash
ssh-keygen -t ed25519 -C "github-actions-panjigautama-hugo" -f ./panjigautama-hugo-deploy -N ""
```

Install the public key on the VPS (one-time; password login OK for this step):

```bash
ssh-copy-id -i ./panjigautama-hugo-deploy.pub root@103.92.215.36
```

Verify:

```bash
ssh -i ./panjigautama-hugo-deploy root@103.92.215.36 'echo ok'
```

GitHub Actions secrets:

| Secret | Value |
|--------|--------|
| `SSH_HOST` | `103.92.215.36` |
| `SSH_USER` | `root` |
| `SSH_PRIVATE_KEY` | Contents of `panjigautama-hugo-deploy` (private) |
| `DEPLOY_PATH` | `/opt/panjigautama-hugo` |

Never commit the private key. Prefer the key over storing the root password in CI.

## Step-by-step: first deploy (Ubuntu)

### 1. SSH to the VPS

```bash
ssh root@103.92.215.36
```

### 2. Ensure Docker network `web`

```bash
docker network ls | grep -w web || docker network create web
```

### 3. Clone repo and submodules

```bash
cd /opt
git clone https://github.com/rhapsodixx/panjigautama-hugo.git panjigautama-hugo
cd /opt/panjigautama-hugo
git submodule update --init --recursive
```

Confirm `site/themes/hugo-bearblog/` is non-empty.

### 4. Build and start

```bash
docker compose build && docker compose up -d
docker compose ps
docker compose logs --tail=50 blog
```

### 5. Smoke-test on network `web`

```bash
docker run --rm --network web curlimages/curl:8.5.0 -sI http://panjigautama-hugo:8080/ | head -1
# Expect: HTTP/1.1 200 OK
```

Do not flip Caddy until this returns 200.

### 6. Merge host Caddy config

```bash
cp /opt/caddy/Caddyfile /opt/caddy/Caddyfile.bak.$(date +%Y%m%d%H%M)
nano /opt/caddy/Caddyfile
```

Replace/update the site block for the blog hosts with the snippet above (upstream `panjigautama-hugo:8080`).

Reload (Caddy-in-Docker; adjust container name if different):

```bash
docker exec caddy caddy validate --config /etc/caddy/Caddyfile
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

### 7. HTTPS smoke

```bash
curl -sI https://panjigautama.com/ | head -1
curl -sI https://blog.kamisamanosumopod.my.id/ | head -1
```

### 8. Stop WordPress / LiteSpeed for this vhost

Stop without deleting data; keep recoverable **48–72 hours**. See [`docs/operations-cutover.md`](../../operations-cutover.md).

## Ongoing deploy automation

### Local script (`scripts/deploy.sh` — to implement)

Uses the same SSH key (or agent) to run on the VPS:

```bash
cd "$DEPLOY_PATH"
git pull
git submodule update --init --recursive
docker compose build && docker compose up -d
```

### GitHub Action (on push to `main` — to implement)

SSH with `appleboy/ssh-action` (or equivalent) and the secrets above; run the same remote commands. First cutover may use the script alone until secrets are configured.

## Error handling

| Failure | Action |
|---------|--------|
| Compose build fails | Fix on VPS or revert commit; do not reload Caddy |
| Curl to container ≠ 200 | Inspect `docker compose logs`; keep prior Caddy upstream |
| Caddy validate fails | Restore `Caddyfile.bak.*`; fix syntax |
| Bad production after flip | Restore prior Caddy block; restart WordPress; optional `docker compose stop` |

## Testing / acceptance

- [ ] Container healthy on `web`; curl via container name returns 200
- [ ] All three hostnames HTTPS 200 after Caddy reload
- [ ] Sample post, page, `/images/`, category paths 200
- [ ] `./scripts/deploy.sh` (or Action) updates site after a content commit
- [ ] Rollback path documented and backup Caddyfile retained

## Implementation follow-ups

1. Update `docker-compose.yml` for external `web` (drop host ports).
2. Update `Caddyfile.snippet` and cutover runbook (done in this change set for docs).
3. Add `scripts/deploy.sh`.
4. Add `.github/workflows/deploy.yml`.
5. Operator: generate deploy key, set GitHub secrets, first install on VPS.
