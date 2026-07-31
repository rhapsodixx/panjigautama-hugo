# VPS Cutover Runbook — WordPress → Hugo

Operator steps to deploy the Hugo blog on the production VPS, switch host Caddy from WordPress/LiteSpeed, and roll back if needed.

**Related:** [ADR-004](./decisions/ADR-004-compose-build-host-caddy.md), [`Caddyfile.snippet`](../Caddyfile.snippet), [`docs/qa-checklist.md`](./qa-checklist.md)

## When to run

- Local Hugo QA is complete ([`docs/qa-checklist.md`](./qa-checklist.md) dated pass).
- You have SSH access to the VPS and permission to edit the host Caddyfile and stop the WordPress/LiteSpeed vhost for `panjigautama.com`.
- Schedule a maintenance window; keep the WordPress stack **stopped but intact** for **48–72 hours** after cutover.

## Important: verify Compose on the VPS first

During Tasks 7 and 8, **local Docker was unavailable** (daemon not running). The Compose image and container were **not** verified locally. Before changing host Caddy:

1. Complete steps 1–4 below (clone, submodules, `docker compose build && up -d`, `curl` to `127.0.0.1:8080`).
2. Only proceed to the Caddy flip (step 5) after the container serves HTTP 200 on localhost.

---

## 1. SSH and sync the repo

```bash
ssh <user>@<vps-host>
```

First deploy:

```bash
git clone https://github.com/rhapsodixx/panjigautama-hugo.git
cd panjigautama-hugo
```

Subsequent deploys:

```bash
cd panjigautama-hugo   # or your chosen install path
git pull
```

## 2. Initialize git submodules

The Bear Blog theme is a submodule; it must be present before the Docker build.

```bash
git submodule update --init --recursive
```

Confirm `site/themes/hugo-bearblog/` exists and is not empty.

## 3. Build and start the container

From the repo root (where `docker-compose.yml` lives):

```bash
docker compose build && docker compose up -d
```

Expected:

- Image builds Hugo in-stage and serves `public/` via in-container Caddy on port `8080`.
- Compose publishes `127.0.0.1:8080:8080` (host Caddy owns public 80/443).

Check container status:

```bash
docker compose ps
docker compose logs --tail=50 blog
```

## 4. Verify the container locally on the VPS

Before touching host Caddy:

```bash
curl -sI http://127.0.0.1:8080/ | head -1
# Expect: HTTP/1.1 200 OK

curl -sI http://127.0.0.1:8080/about-me/ | head -1
curl -sI http://127.0.0.1:8080/blog/ | head -1
```

If build or curl fails, **stop here**. Do not merge the Caddy snippet. Fix Compose/logs first.

---

## 5. Merge host Caddy config and reload

**Back up** the current `panjigautama.com` site block in the host Caddyfile (you need it for rollback).

Replace or update the site block with the contents of [`Caddyfile.snippet`](../Caddyfile.snippet):

```caddy
panjigautama.com, www.panjigautama.com {
	encode gzip
	reverse_proxy 127.0.0.1:8080
}
```

Validate and reload (adjust paths/commands for your install):

```bash
# Example — use your host’s Caddy binary and config path
caddy validate --config /etc/caddy/Caddyfile
caddy reload --config /etc/caddy/Caddyfile
```

Systemd-managed Caddy (common on Linux):

```bash
sudo systemctl reload caddy
# or: sudo caddy reload --config /etc/caddy/Caddyfile
```

Confirm HTTPS from the VPS or your workstation:

```bash
curl -sI https://panjigautama.com/ | head -1
```

---

## 6. Stop WordPress and LiteSpeed (do not delete)

Stop the WordPress/LiteSpeed vhost for `panjigautama.com` **without deleting** databases, files, or containers.

Examples (adapt to your stack):

```bash
# LiteSpeed / OpenLiteSpeed — disable the vhost or stop the site listener
# WordPress — stop PHP-FPM pool or the WP container for this site only
# Do NOT: rm -rf wp-content, drop MySQL databases, or prune volumes
```

Document what you stopped and where data lives. Keep everything recoverable for **48–72 hours**.

---

## 7. Production smoke checks

Run after Caddy points at Hugo. See also [`docs/qa-checklist.md`](./qa-checklist.md).

| Check | Command / action | Expected |
|-------|------------------|----------|
| HTTPS homepage | `curl -sI https://panjigautama.com/` | `200` |
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
for p in / /blog/ /muhasabah/ /about-me/ /images/favicon.png /categories/meeting/; do
  echo -n "$p "
  curl -s -o /dev/null -w "%{http_code}\n" "https://panjigautama.com$p"
done
```

---

## 8. Rollback (within 48–72 h window)

If production checks fail or you need to revert:

1. **Restore the prior Caddy site block** for `panjigautama.com` (from backup in step 5) so it reverse-proxies to the WordPress/LiteSpeed upstream again.
2. Reload Caddy:

   ```bash
   caddy reload --config /etc/caddy/Caddyfile
   # or: sudo systemctl reload caddy
   ```

3. **Start WordPress/LiteSpeed** for the vhost (reverse of step 6).
4. **Stop the Hugo container** (optional but avoids port confusion on localhost):

   ```bash
   cd panjigautama-hugo
   docker compose stop
   ```

5. Re-run smoke checks against `https://panjigautama.com/` to confirm WordPress is serving again.

After the rollback window expires and Hugo is stable, decommission WordPress/LiteSpeed for this site in a separate, deliberate step.

---

## Post-cutover

- Monitor GA4 and server logs for 48–72 hours.
- After the rollback window, remove or archive the WordPress stack if no longer needed.
- Future content updates: `git pull`, `git submodule update --init --recursive`, `docker compose build && docker compose up -d`.
