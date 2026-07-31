# ADR-004: Build Hugo with Docker Compose on the VPS; reverse-proxy via host Caddy

## Status
Accepted

## Date
2026-07-31

## Revised
2026-07-31 — Align with sumopod Vaultwarden pattern: external Docker network `web`, Caddy proxies by container name; git-based content updates; local deploy script + GitHub Action. See [deploy design](../superpowers/specs/2026-07-31-vps-compose-caddy-deploy-design.md).

2026-07-31 — Production on sumopod (`103.92.215.36`): `/opt/panjigautama-hugo` live; host Caddy container `caddy-caddy-1`; GitHub Actions secrets configured (SSH deploy key). Alias `blog.kamisamanosumopod.my.id` serves Hugo over HTTPS. Apex/www remain on the previous host until DNS cutover (add them to the Caddy site block only after A/AAAA point at sumopod, to avoid ACME failures). Host-fingerprint pin in appleboy/ssh-action deferred (mismatch against known-good OpenSSH SHA256 fingerprints).

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
- Ongoing deploys: `git pull --ff-only` + submodule update + `compose build && up`, via `scripts/deploy.sh` and/or GitHub Action `.github/workflows/deploy.yml` on push to `main`.
- CI authenticates with an SSH **deploy key** (never store the root password or private key in the git repo). Optional host-fingerprint pinning via appleboy is deferred until it accepts this host’s keys reliably.

Provide a `Caddyfile.snippet` documenting the **target** site block (all public hostnames). Production may temporarily list only hostnames whose DNS already points at sumopod.

**Which hostnames** appear on that block, and whether aliases redirect or serve content, is decided in [ADR-005](./ADR-005-multi-domain-aliases.md).

### GitHub Actions secrets (repo `panjigautama-hugo`)

| Secret | Purpose |
|--------|---------|
| `SSH_HOST` | VPS IP / hostname (`103.92.215.36`) |
| `SSH_USER` | SSH user (`root`) |
| `SSH_PRIVATE_KEY` | Deploy private key PEM (set via `gh secret set`, never commit) |
| `DEPLOY_PATH` | `/opt/panjigautama-hugo` |
| `SSH_HOST_FINGERPRINT` | Optional; intended for appleboy host-key pin. **Not wired in the workflow today** — drone-ssh reported fingerprint mismatch for all correct OpenSSH SHA256 host-key fingerprints on this VPS (2026-07-31). Revisit when multi-algo pinning works; rely on fixed IP + deploy key until then. |

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
- Partially revisited in ops: alias hostname went live on sumopod first; apex DNS cutover is a separate step so ACME only runs for hostnames that already resolve here

## Consequences
- Deploy docs must cover Compose on `web`, host Caddy reload (`docker exec caddy-caddy-1 caddy reload …`), SSH deploy key setup, fingerprint secret, and the local script / GitHub Action
- Blog container must join `web` and must not publish public 80/443
- Hostname list and alias policy: see ADR-005 (canonical Hugo `baseURL` remains the apex)
- Until apex DNS moves, only list resolving hostnames in the live Caddyfile; keep `Caddyfile.snippet` as the full target list
- Rollback for apex = leave DNS/WordPress on the previous host; for the alias = restore prior Caddyfile backup and/or stop the Hugo container
- New posts/edits require a git push to `main` (Action) or `./scripts/deploy.sh`, not a WordPress admin UI
- Private keys and `.env` files must stay out of git (`.gitignore`); rotate the deploy key if it is ever committed or leaked
