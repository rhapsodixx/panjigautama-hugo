# VPS Cutover Runbook — WordPress → Hugo

Operator steps to deploy the Hugo blog on the sumopod VPS, switch host Caddy from WordPress/LiteSpeed, and roll back if needed.

**Related:** [ADR-004](./decisions/ADR-004-compose-build-host-caddy.md), [deploy design](./superpowers/specs/2026-07-31-vps-compose-caddy-deploy-design.md), [`Caddyfile.snippet`](../Caddyfile.snippet), [`docs/qa-checklist.md`](./qa-checklist.md)

**Host:** `103.92.215.36` (Ubuntu) · **Install path:** `/opt/panjigautama-hugo` · **Network:** Docker `web`

## When to run

- Local Hugo QA is complete ([`docs/qa-checklist.md`](./qa-checklist.md) dated pass).
- You have SSH access to the VPS and permission to edit `/opt/caddy/Caddyfile` and stop the WordPress/LiteSpeed vhost for `panjigautama.com`.
- Schedule a maintenance window; keep the WordPress stack **stopped but intact** for **48–72 hours** after cutover.

## Important: verify Compose on the VPS first

Before changing host Caddy:

1. Complete clone → submodule → `docker compose build && up -d`.
2. Confirm HTTP 200 via `http://panjigautama-hugo:8080/` **on network `web`**.
3. Only then merge the Caddy snippet and reload.

---

## 0. SSH deploy key + GitHub Actions secrets (once)

On a trusted machine (do **not** commit the private key; keep it outside the repo or gitignored):

```bash
ssh-keygen -t ed25519 -C "github-actions-panjigautama-hugo" -f ./panjigautama-hugo-deploy -N ""
ssh-copy-id -i ./panjigautama-hugo-deploy.pub root@103.92.215.36
ssh -i ./panjigautama-hugo-deploy root@103.92.215.36 'echo ok'
```

Host fingerprint (for Action host-key verification):

```bash
ssh-keyscan -t ed25519 103.92.215.36 2>/dev/null | ssh-keygen -lf -
# Example form: 256 SHA256:… 103.92.215.36 (ED25519)
# Use the SHA256:… value as SSH_HOST_FINGERPRINT
```

Set GitHub Actions secrets with the CLI (values go to GitHub only — never commit them):

```bash
gh secret set SSH_HOST -R rhapsodixx/panjigautama-hugo --body '103.92.215.36'
gh secret set SSH_USER -R rhapsodixx/panjigautama-hugo --body 'root'
gh secret set DEPLOY_PATH -R rhapsodixx/panjigautama-hugo --body '/opt/panjigautama-hugo'
gh secret set SSH_HOST_FINGERPRINT -R rhapsodixx/panjigautama-hugo --body 'SHA256:…'
gh secret set SSH_PRIVATE_KEY -R rhapsodixx/panjigautama-hugo < ./panjigautama-hugo-deploy
gh secret list -R rhapsodixx/panjigautama-hugo
```

Workflow: [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml) (push to `main` or `workflow_dispatch`). Prefer the deploy key over putting the root password in CI. See [ADR-004](./decisions/ADR-004-compose-build-host-caddy.md).

### Production note (2026-07-31)

- Hugo container is live on sumopod; Caddy (`caddy-caddy-1`) serves **https://blog.kamisamanosumopod.my.id/**.
- Apex `panjigautama.com` / `www` still resolve to the previous host until DNS cutover — do not add them to the live Caddyfile until A/AAAA point at `103.92.215.36`.

---

## 1. SSH to the VPS

```bash
ssh root@103.92.215.36
```

---

## 2. Ensure Docker network `web`

```bash
docker network ls | grep -w web || docker network create web
```

---

## 3. Clone repo and initialize submodules

First deploy:

```bash
cd /opt
git clone https://github.com/rhapsodixx/panjigautama-hugo.git panjigautama-hugo
cd /opt/panjigautama-hugo
git submodule update --init --recursive
```

Subsequent deploys (manual):

```bash
cd /opt/panjigautama-hugo
git pull
git submodule update --init --recursive
```

Confirm `site/themes/hugo-bearblog/` exists and is not empty.

---

## 4. Build and start the container

From `/opt/panjigautama-hugo` (where `docker-compose.yml` lives):

```bash
docker compose build && docker compose up -d
docker compose ps
docker compose logs --tail=50 blog
```

Expected:

- Image builds Hugo in-stage and serves `public/` via in-container Caddy on port `8080`.
- Container joins external network `web` (no host port publish).
- `container_name` is `panjigautama-hugo`.

---

## 5. Verify on Docker network `web`

Before touching host Caddy:

```bash
docker run --rm --network web curlimages/curl:8.5.0 -sI http://panjigautama-hugo:8080/ | head -1
# Expect: HTTP/1.1 200 OK

docker run --rm --network web curlimages/curl:8.5.0 -sI http://panjigautama-hugo:8080/about-me/ | head -1
docker run --rm --network web curlimages/curl:8.5.0 -sI http://panjigautama-hugo:8080/blog/ | head -1
```

If build or curl fails, **stop here**. Do not merge the Caddy snippet. Fix Compose/logs first.

---

## 6. Merge host Caddy config and reload

**Back up** the current site block for `panjigautama.com` (needed for rollback):

```bash
cp /opt/caddy/Caddyfile /opt/caddy/Caddyfile.bak.$(date +%Y%m%d%H%M)
nano /opt/caddy/Caddyfile
```

Replace or update the site block with [`Caddyfile.snippet`](../Caddyfile.snippet):

```caddy
panjigautama.com, www.panjigautama.com, blog.kamisamanosumopod.my.id {
	encode gzip
	reverse_proxy panjigautama-hugo:8080
}
```

Host Caddy must be on Docker network `web` so the name `panjigautama-hugo` resolves (same pattern as Vaultwarden).

**DNS:** point `blog.kamisamanosumopod.my.id` at this VPS before Caddy can issue its certificate. Apex/`www` as already configured.

Validate and reload (sumopod Compose service name → container `caddy-caddy-1`):

```bash
docker exec caddy-caddy-1 caddy validate --config /etc/caddy/Caddyfile
docker exec caddy-caddy-1 caddy reload --config /etc/caddy/Caddyfile
```

If Caddy is managed by systemd on the host instead:

```bash
caddy validate --config /opt/caddy/Caddyfile
systemctl reload caddy
```

Confirm HTTPS:

```bash
curl -sI https://panjigautama.com/ | head -1
curl -sI https://blog.kamisamanosumopod.my.id/ | head -1
```

Note: Hugo `baseURL` stays `https://panjigautama.com`, so some absolute links in HTML still point at the apex domain. Paths and content work on both hosts.

---

## 7. Stop WordPress and LiteSpeed (do not delete)

Stop the WordPress/LiteSpeed vhost for `panjigautama.com` **without deleting** databases, files, or containers.

Examples (adapt to your stack):

```bash
# LiteSpeed / OpenLiteSpeed — disable the vhost or stop the site listener
# WordPress — stop PHP-FPM pool or the WP container for this site only
# Do NOT: rm -rf wp-content, drop MySQL databases, or prune volumes
```

Document what you stopped and where data lives. Keep everything recoverable for **48–72 hours**.

---

## 8. Production smoke checks

Run after Caddy points at Hugo. See also [`docs/qa-checklist.md`](./qa-checklist.md).

| Check | Command / action | Expected |
|-------|------------------|----------|
| HTTPS homepage | `curl -sI https://panjigautama.com/` | `200` |
| Alias domain homepage | `curl -sI https://blog.kamisamanosumopod.my.id/` | `200` |
| Sample posts | `/muhasabah/`, `/api-key-best-practices/`, `/silent-meeting/` | `200`, content renders |
| Static pages | `/about-me/`, `/privacy-policy/` | `200` |
| Blog index | `/blog/` | `200`, post list |
| Category | `/categories/meeting/` | `200`, lists posts |
| Favicon | Browser or `curl -sI https://panjigautama.com/images/favicon.png` | `200` |
| In-content image | e.g. `/images/Screenshot-2025-01-21-at-10.18.40.png` | `200` |
| Google Analytics 4 | View page source or DevTools → Network | Request to `googletagmanager.com` / gtag with `G-60P3WJPWMJ` |
| Old media path | `/wp-content/uploads/test.jpg` | `404` (acceptable per ADR-003) |

Quick curl loop:

```bash
for host in https://panjigautama.com https://blog.kamisamanosumopod.my.id; do
  echo "== $host =="
  for p in / /blog/ /muhasabah/ /about-me/ /images/favicon.png /categories/meeting/; do
    echo -n "$p "
    curl -s -o /dev/null -w "%{http_code}\n" "$host$p"
  done
done
```

---

## 9. Rollback (within 48–72 h window)

If production checks fail or you need to revert:

1. **Restore the prior Caddy site block** from the backup in step 6.
2. Reload Caddy:

   ```bash
   docker exec caddy-caddy-1 caddy reload --config /etc/caddy/Caddyfile
   # or: systemctl reload caddy
   ```

3. **Start WordPress/LiteSpeed** for the vhost (reverse of step 7).
4. **Stop the Hugo container** (optional):

   ```bash
   cd /opt/panjigautama-hugo
   docker compose stop
   ```

5. Re-run smoke checks against `https://panjigautama.com/` to confirm WordPress is serving again.

After the rollback window expires and Hugo is stable, decommission WordPress/LiteSpeed for this site in a separate, deliberate step.

---

## Post-cutover / new posts

- Monitor GA4 and server logs for 48–72 hours.
- After the rollback window, remove or archive the WordPress stack if no longer needed.
- **New or edited posts:** edit Markdown locally → commit → push `main` → deploy:

  ```bash
  # On VPS (or via scripts/deploy.sh / GitHub Action):
  cd /opt/panjigautama-hugo
  git pull
  git submodule update --init --recursive
  docker compose build && docker compose up -d
  ```

- No Docker Hub. The VPS always builds from git ([ADR-004](./decisions/ADR-004-compose-build-host-caddy.md)).
