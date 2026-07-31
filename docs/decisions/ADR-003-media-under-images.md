# ADR-003: Store media under `/images/` and rewrite content references

## Status
Accepted

## Date
2026-07-31

## Context
WordPress media lives under `/wp-content/uploads/YYYY/MM/...`. After migration, keeping that path would either require mirroring the old tree under `static/wp-content/` or serving compatibility redirects. The preferred site shape is a clean static tree.

## Decision
Download media into `site/static/images/` and rewrite in-post/in-page references from `/wp-content/uploads/...` (and absolute `panjigautama.com/wp-content/...` URLs) to `/images/<filename>` (with light namespacing if needed to avoid collisions).

Do **not** add permanent redirects from `/wp-content/uploads/...` to the new paths. Only rewritten content links are required to work.

## Alternatives Considered

### Preserve `/wp-content/uploads/` tree under `static/`
- Pros: Zero rewrite; external hotlinks keep working
- Cons: Carries WordPress path conventions into Hugo forever
- Rejected: Prefer cleaner static layout

### Rewrite content and add `/wp-content/` → `/images/` redirects
- Pros: Softens breakage for external hotlinks and Google Images
- Cons: Redirect map maintenance; rejected by product choice for v1
- Rejected: Explicit “no old media URL redirects” decision

## Consequences
- Converter must download files and rewrite HTML/Markdown reliably
- External bookmarks to old media URLs will 404
- Favicon is fetched from the live WP URL once, then served from Hugo `static/`
