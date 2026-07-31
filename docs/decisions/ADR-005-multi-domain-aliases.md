# ADR-005: Serve alias domains on the same Hugo site (no redirect)

## Status
Accepted

## Date
2026-07-31

## Context
The blog’s primary brand domain is `panjigautama.com`. An additional hostname, `blog.kamisamanosumopod.my.id`, should also reach the same content after the WordPress → Hugo cutover. Host Caddy already terminates TLS and reverse-proxies to the Compose blog container ([ADR-004](./ADR-004-compose-build-host-caddy.md)).

Requirements:
- Both hostnames must return the live Hugo site over HTTPS
- Prefer minimal ops (one container, one site block)
- Keep a single canonical site identity for feeds, sitemap, and social cards

## Decision
List all serving hostnames on **one** host Caddy site block that reverse-proxies to `127.0.0.1:8080`:

- `panjigautama.com`
- `www.panjigautama.com`
- `blog.kamisamanosumopod.my.id`

Document the block in `Caddyfile.snippet` and the cutover runbook.

Hugo `baseURL` remains `https://panjigautama.com` (canonical). Absolute links, Open Graph, and sitemap keep that apex; path routing works on every listed hostname.

## Alternatives Considered

### Redirect alias → apex (301)
- Pros: Stronger single-canonical SEO; no dual-host absolute-URL confusion
- Cons: Extra hop for visitors of `blog.kamisamanosumopod.my.id`; alias never “stays” as a live URL
- Rejected: Explicit product choice to **serve** both domains (option A), not redirect (option B)

### Separate containers / site blocks per domain
- Pros: Independent config or versions per host
- Cons: Duplicate deploy surface with no benefit for identical content
- Rejected: YAGNI

### `relativeURLs = true` so every host is fully self-referential
- Pros: Built HTML does not hardcode the apex
- Cons: Trade-offs for RSS, some absolute URL consumers, and social previews
- Rejected for now: keep canonical `baseURL`; revisit if alias-domain absolute links become a problem

## Consequences
- DNS for `blog.kamisamanosumopod.my.id` must point at the VPS before Caddy can issue its certificate
- Smoke tests should cover both apex and alias hostnames ([`docs/operations-cutover.md`](../operations-cutover.md))
- Adding or removing a hostname is a Caddyfile change only (no Hugo rebuild required for routing)
- Search engines may see two hosts with overlapping content; if that becomes an issue, supersede this ADR with a redirect-to-canonical policy
