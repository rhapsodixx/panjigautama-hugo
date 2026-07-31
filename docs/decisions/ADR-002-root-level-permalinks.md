# ADR-002: Preserve root-level post and page permalinks

## Status
Accepted

## Date
2026-07-31

## Context
WordPress pretty permalinks serve posts and pages at the site root, e.g. `https://panjigautama.com/muhasabah/` and `https://panjigautama.com/about-me/`. Hugo Bear Blog’s example layout places posts under a `blog` section, which would default to `/blog/<slug>/` unless configured otherwise.

Existing links, search results, and reader bookmarks depend on root-level paths.

## Decision
Keep public URLs at `/<slug>/` for posts and pages. Implement via Hugo permalink configuration (and/or front matter) so content may live under `content/blog/` internally while publishing at the root path.

## Alternatives Considered

### Bear Blog default `/blog/<slug>/` plus redirects
- Pros: Less Hugo config
- Cons: Extra redirect layer; dual URL forms forever
- Rejected: Prefer canonical URLs matching WordPress

### Ignore old URLs
- Pros: Simplest
- Cons: Breaks SEO and inbound links
- Rejected: Explicit requirement to preserve root-level URLs

## Consequences
- `hugo.toml` permalinks (or equivalent) are a critical config surface
- Converter must emit stable slugs matching WordPress `post_name`
- Category taxonomy URLs may still use Hugo defaults (e.g. `/categories/...`) unless later customized
