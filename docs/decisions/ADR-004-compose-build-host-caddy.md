# ADR-004: Build Hugo with Docker Compose on the VPS; reverse-proxy via host Caddy

## Status
Accepted

## Date
2026-07-31

## Context
The production VPS already runs Caddy as the TLS/edge reverse proxy and hosts other apps in Docker. The blog should fit that model rather than introducing a second public web server or replacing Caddy.

Validation happens locally first; production cutover happens in a maintenance window after QA.

## Decision
Use a multi-stage Dockerfile: build the Hugo site in one stage, serve `public/` with a small static server in the runtime stage. On the VPS, `docker compose build && up` produces and runs the container. Host Caddy terminates HTTPS for the blog’s public hostnames and reverse-proxies to the container’s internal port (`127.0.0.1:8080`).

Provide a `Caddyfile.snippet` documenting the site block to merge into the host Caddy config.

**Which hostnames** appear on that block, and whether aliases redirect or serve content, is decided in [ADR-005](./ADR-005-multi-domain-aliases.md).

## Alternatives Considered

### Build in CI / locally and ship only `public/`
- Pros: Smaller runtime image; no Hugo in prod build
- Cons: Extra artifact pipeline; diverges from “build on VPS via Compose” preference
- Rejected: Operator preference is Compose build-on-VPS

### Container Caddy binds :443 directly
- Pros: Self-contained TLS
- Cons: Conflicts with existing host Caddy and other apps
- Rejected: Host Caddy remains the edge

### Run Hugo beside WordPress and flip DNS gradually
- Pros: Parallel validation on production domain pieces
- Cons: More moving parts; staging preference is local-then-cutover
- Rejected: Chosen cutover is local QA then production swap

## Consequences
- Deploy docs must cover Compose **and** host Caddy reload
- Container must not publish conflicting public 80/443 if host Caddy owns them
- Hostname list and alias policy: see ADR-005 (canonical Hugo `baseURL` remains the apex)
- Rollback = repoint Caddy to WordPress/LiteSpeed while that stack remains recoverable (~48–72h)
