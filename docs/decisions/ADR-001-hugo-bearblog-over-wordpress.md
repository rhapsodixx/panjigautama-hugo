# ADR-001: Use Hugo with hugo-bearblog instead of WordPress

## Status
Accepted

## Date
2026-07-31

## Context
panjigautama.com runs on a VPS with WordPress and LiteSpeed. The site is a personal blog (~45 posts, a few pages). WordPress adds PHP, database, plugin, and security maintenance overhead for a content workload that is mostly static. The VPS already runs other apps with Docker and host Caddy.

Goals:
- Simpler ops (static files, no MySQL)
- Fast pages and predictable deploys
- Minimal, readable blog UI
- Fit the existing Docker + Caddy hosting model

## Decision
Rebuild the blog as a Hugo static site using the [hugo-bearblog](https://github.com/janraasch/hugo-bearblog) theme (light default), hosted in Docker behind the existing host Caddy.

## Alternatives Considered

### Keep WordPress + LiteSpeed
- Pros: No migration; familiar admin UI
- Cons: Ongoing PHP/DB/plugin patching; heavier than needed for a personal blog
- Rejected: Ops cost outweighs benefit for this content profile

### Other SSGs (Astro, Eleventy, Jekyll)
- Pros: Modern ecosystems
- Cons: Extra framework choice without a clear win for Markdown blogging; Hugo’s speed and single-binary build fit VPS Compose well
- Rejected: Hugo + Bear Blog is the explicit product choice

### Heavier Hugo themes
- Pros: More features out of the box
- Cons: Conflicts with the desired no-nonsense Bear Blog aesthetic
- Rejected: Theme choice is intentional

## Consequences
- Content becomes Git-managed Markdown
- Publishing requires a build/deploy step instead of WP admin
- Comments and WP plugins are not carried over in v1
- Migration needs a one-time WXR → Markdown pipeline
