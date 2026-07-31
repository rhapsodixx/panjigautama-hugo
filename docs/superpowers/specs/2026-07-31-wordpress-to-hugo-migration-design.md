# WordPress → Hugo Migration Design — panjigautama.com

**Date:** 2026-07-31  
**Status:** Approved  
**Repo:** `panjigautama-hugo` (public)

## Goal

Migrate the self-hosted WordPress + LiteSpeed blog at [panjigautama.com](https://panjigautama.com) to [Hugo](https://gohugo.io/) with the [hugo-bearblog](https://github.com/janraasch/hugo-bearblog) theme (light scheme), served via Docker behind the existing VPS host Caddy. Preserve root-level post/page URLs. Install Google Analytics `G-60P3WJPWMJ` and the existing site favicon.

## Decisions (summary)

| Topic | Choice |
|-------|--------|
| Cutover | Local validate first, then production |
| URLs | Keep WordPress root-level paths (`/<slug>/`) |
| Media | Move to `/images/...`, rewrite in-content references |
| Old media URLs | No `/wp-content/` redirects |
| Comments | Drop for v1; third-party later optional |
| Deploy | `docker compose` builds Hugo on VPS; host Caddy reverse-proxies |
| Categories | Hugo taxonomies with term index pages |
| Conversion | Scripted WXR → Markdown pipeline |

See `docs/decisions/` for full ADRs.

## Source inventory

From `wordpress-backup/` (WXR, 2026-07-31):

- **45** published posts
- **3** published pages: About Me, Privacy Policy, Engineering Lead Materials
- **81** media items
- Drafts (e.g. Sprout Test) and `inherit` attachment stubs are **not** migrated as content
- Favicon candidates on live site: `/wp-content/uploads/2021/01/ico.png` and cropped variants

## Architecture

```text
panjigautamacom-blog/   (GitHub: panjigautama-hugo)
├── AGENTS.md
├── CLAUDE.md
├── wordpress-backup/          # source WXR
├── scripts/                   # WXR → Markdown + media downloader/rewriter
├── site/                      # Hugo project root
│   ├── hugo.toml
│   ├── content/
│   ├── static/images/
│   ├── static/favicon.*
│   ├── layouts/partials/      # custom_head (GA + favicon)
│   └── themes/hugo-bearblog/  # git submodule
├── Dockerfile
├── docker-compose.yml
├── Caddyfile.snippet
└── docs/
    ├── decisions/             # ADRs
    └── superpowers/specs/     # this design
```

### Runtime

- **Local:** `hugo server` in `site/` for content QA; optional `docker compose up` to prove the image.
- **VPS:** Host Caddy terminates TLS and reverse-proxies `panjigautama.com` to the blog container. Compose builds Hugo inside the image and serves `public/` on an internal port. WordPress/LiteSpeed for this vhost are retired at cutover.

### Out of scope (v1)

- Comment migration or Giscus/Utterances setup
- `/wp-content/uploads/` compatibility redirects
- Automated staging subdomain

## Content migration pipeline

1. Parse posts, pages, and media WXR files.
2. Keep only **published** posts and pages.
3. Write Markdown:
   - Posts → `site/content/blog/<slug>.md` with permalinks configured so public URLs are `/<slug>/`
   - Pages → `site/content/<slug>.md`
4. Front matter: `title`, `date`, `lastmod`, `draft`, `categories`, `tags` (if any), `slug`.
5. Download media from live `panjigautama.com` into `site/static/images/` (flatten or lightly namespaced to avoid collisions).
6. Rewrite body image `src` from `/wp-content/uploads/...` (and absolute WP URLs) → `/images/...`.
7. Convert WP HTML to Markdown where reliable; leave complex HTML intact if conversion would be lossy.
8. Do not export comments.

### Site / theme configuration

- Theme: `hugo-bearblog` as git submodule
- Light default (theme’s system dark via `prefers-color-scheme` is acceptable; do not force dark)
- Favicon from live site → `static/` + links in `layouts/partials/custom_head.html`
- GA4 `G-60P3WJPWMJ` via gtag in `custom_head.html`
- Category taxonomies enabled (list + term pages)

## Docker and cutover

### Image

1. Build stage: official Hugo image → `hugo --minify`
2. Serve stage: lightweight static server (Caddy or nginx in-container) on e.g. `:8080`

### Compose (VPS)

- Service `blog`: build from repo, restart policy, not bound to public 80/443
- Host Caddy site block (documented in `Caddyfile.snippet`):

```caddy
panjigautama.com {
    reverse_proxy <blog-upstream>:8080
}
```

### Deploy sequence

1. Clone/pull `panjigautama-hugo` on VPS
2. `docker compose build && docker compose up -d`
3. Merge/reload host Caddy with snippet
4. Stop/disable WordPress + LiteSpeed for this site
5. Verify HTTPS, sample post URLs, favicon, GA

### Rollback

Keep WordPress stack stopped but recoverable for 48–72 hours; repoint Caddy if needed.

## Error handling

- Media download failures: log URL, continue, print missing list for retry
- Slug collisions or empty titles: fail the converter with a clear error
- Failed Hugo/Compose build: do not deploy a half-built `public/`

## Testing / success criteria

- All 45 published posts and 3 pages render at root URLs
- Category term pages work
- In-post images load from `/images/...`
- Favicon and GA (`G-60P3WJPWMJ`) present on production
- HTTPS via existing host Caddy

## Step-by-step migration

1. Create public GitHub repo `panjigautama-hugo`; init local git
2. Add `AGENTS.md`, `CLAUDE.md`, and ADRs
3. Scaffold Hugo site + Bear Blog submodule; configure root permalinks and taxonomies
4. Implement and run WXR converter (Markdown + media rewrite)
5. Add favicon and GA4
6. Local QA with `hugo server`
7. Add Dockerfile, `docker-compose.yml`, `Caddyfile.snippet`; verify Compose locally
8. VPS deploy and cutover
9. Post-cutover smoke test; hold WP rollback window

## Agent documentation

- `AGENTS.md` references `CLAUDE.md` as the source of truth for stack and conventions
- `CLAUDE.md` lists stack, docs map, and requires ADR review before significant changes
