# panjigautama-hugo

Personal blog for [panjigautama.com](https://panjigautama.com), migrating from WordPress to Hugo.

## Stack

| Layer | Choice |
|-------|--------|
| Site generator | [Hugo](https://gohugo.io/) |
| Theme | [hugo-bearblog](https://github.com/janraasch/hugo-bearblog) (light default) |
| Content | Markdown from WordPress WXR (`wordpress-backup/`) |
| Media | `site/static/images/`; in-content URLs rewritten from `/wp-content/uploads/` |
| Analytics | Google Analytics 4 — measurement ID `G-60P3WJPWMJ` |
| Favicon | Copied from live panjigautama.com into Hugo `static/` |
| Local serve | `hugo server` (site root under `site/`) |
| Production | Docker multi-stage build + Compose on VPS |
| Edge | Existing host **Caddy** reverse-proxy (TLS) → blog container |
| Domains | `panjigautama.com`, `www.panjigautama.com`, `blog.kamisamanosumopod.my.id` (same site; canonical `baseURL` = panjigautama.com) |
| Repo | Public GitHub: `panjigautama-hugo` |

## Documentation

| Doc | Purpose |
|-----|---------|
| [`AGENTS.md`](./AGENTS.md) | Entry point for agents; points here |
| [`docs/superpowers/specs/2026-07-31-wordpress-to-hugo-migration-design.md`](./docs/superpowers/specs/2026-07-31-wordpress-to-hugo-migration-design.md) | Approved migration design |
| [`docs/decisions/`](./docs/decisions/) | Architecture Decision Records (ADRs) |
| `Caddyfile.snippet` | Host Caddy site-block example (added during implementation) |

## Project layout (target)

```text
wordpress-backup/   # WXR exports (posts, pages, media)
scripts/            # WXR → Markdown + media pipeline
site/               # Hugo project (content, static, theme submodule)
docs/decisions/     # ADRs
docs/superpowers/   # Specs and plans
```

## Conventions

- Public post/page URLs stay **root-level**: `/<slug>/`
- Do **not** add `/wp-content/` redirects unless a new ADR supersedes ADR-003
- Comments are out of scope for v1 (third-party later is fine)
- Prefer editing Markdown/content and config over theme forks; use Bear Blog `custom_head` / partials for GA, favicon, fonts, and pagination chrome
- Multi-host aliases serve the same site; canonical `baseURL` is `https://panjigautama.com` (ADR-005)
- Homepage presentation (Outfit, bulleted titles, Hugo pagination): ADR-006

## Before Making Changes

**Check ADRs first**: Before significant modifications, review the ADR list below for relevant architectural decisions and read them for context.

### ADR index

| ADR | Title |
|-----|-------|
| [ADR-001](./docs/decisions/ADR-001-hugo-bearblog-over-wordpress.md) | Hugo + hugo-bearblog over WordPress |
| [ADR-002](./docs/decisions/ADR-002-root-level-permalinks.md) | Root-level permalinks |
| [ADR-003](./docs/decisions/ADR-003-media-under-images.md) | Media under `/images/` (no `/wp-content/` redirects) |
| [ADR-004](./docs/decisions/ADR-004-compose-build-host-caddy.md) | Compose build on VPS + host Caddy reverse proxy |
| [ADR-005](./docs/decisions/ADR-005-multi-domain-aliases.md) | Multi-domain aliases serve same site (no redirect) |
| [ADR-006](./docs/decisions/ADR-006-homepage-presentation.md) | Homepage: Outfit, bullets, Hugo pagination |

If a change contradicts an ADR, update or supersede the ADR before implementing.
