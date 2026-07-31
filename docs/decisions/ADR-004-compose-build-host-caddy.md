# ADR-004: Build Hugo with Docker Compose on the VPS; reverse-proxy via host Caddy

## Status
Accepted

## Date
2026-07-31

## Revised
2026-07-31 — Align with sumopod Vaultwarden pattern: external Docker network `web`, Caddy proxies by container name; git-based content updates; local deploy script + GitHub Action. See [deploy design](../superpowers/specs/2026-07-31-vps-compose-caddy-deploy-design.md).

## Context
The production VPS (sumopod, Ubuntu) already runs Caddy as the TLS/edge reverse proxy and hosts other apps in Docker Compose on an external network named `web` (e.g. Vaultwarden: Caddy `reverse_proxy vaultwarden:80`). The blog should fit that model rather than introducing a second public web server, a container registry, or host-port publishing.

Validation happens locally first; production cutover happens in a maintenance window after QA. Later content changes are Markdown in git, then rebuild on the VPS.

## Decision
Use a multi-stage Dockerfile: build the Hugo site in one stage, serve `public/` with in-container Caddy on port `8080` in the runtime stage.

On the VPS:

- Install at `/opt/panjigautama-hugo` (git clone).
- `docker compose build && up` builds and runs the container on the **external** Docker network `web`.
- Do **not** publish host ports; host Caddy (also on `web`) reverse-proxies `panjigautama-hugo:8080`.
- Do **not** push images to Docker Hub / GHCR; the VPS builds from git.
- Ongoing deploys: `git pull` + submodule update + `compose build && up`, via `scripts/deploy.sh` and/or a GitHub Action on push to `main`, authenticated with an SSH deploy key (not a password in CI).

Provide a `Caddyfile.snippet` documenting the site block to merge into the host Caddy config (`/opt/caddy/Caddyfile` on sumopod).

**Which hostnames** appear on that block, and whether aliases redirect or serve content, is decided in [ADR-005](./ADR-005-multi-domain-aliases.md).

## Alternatives Considered

### Build in CI / locally and ship only `public/` or a registry image
- Pros: Smaller/faster VPS step; no Hugo toolchain on the server during deploy
- Cons: Extra artifact pipeline and registry credentials; diverges from build-on-VPS preference for a single personal blog
- Rejected: Operator preference is Compose build-on-VPS from git

### Publish `127.0.0.1:8080:8080` and Caddy → localhost
- Pros: Works if Caddy is a host binary outside Docker
- Cons: Diverges from existing sumopod apps on `web`; unnecessary port on the host
- Rejected: Host Caddy resolves peers by container name on `web` (same as Vaultwarden)

### Container Caddy binds :443 directly
- Pros: Self-contained TLS
- Cons: Conflicts with existing host Caddy and other apps
- Rejected: Host Caddy remains the edge

### Run Hugo beside WordPress and flip DNS gradually
- Pros: Parallel validation on production domain pieces
- Cons: More moving parts; staging preference is local-then-cutover
- Rejected: Chosen cutover is local QA then production swap

## Consequences
- Deploy docs must cover Compose on `web`, host Caddy reload, SSH deploy key setup, and the local script / GitHub Action
- Blog container must join `web` and must not publish public 80/443
- Hostname list and alias policy: see ADR-005 (canonical Hugo `baseURL` remains the apex)
- Rollback = repoint Caddy to WordPress/LiteSpeed while that stack remains recoverable (~48–72h)
- New posts/edits require a git push and a VPS rebuild (automated or scripted), not a WordPress admin UI
