# ADR-006: Homepage presentation — Outfit, bulleted posts, Hugo pagination

## Status
Accepted

## Date
2026-07-31

## Context
After migrating to [hugo-bearblog](https://github.com/janraasch/hugo-bearblog) ([ADR-001](./ADR-001-hugo-bearblog-over-wordpress.md)), the stock homepage only rendered `_index.md` content. The live WordPress home listed recent posts. Operators also wanted a clearer typeface and a simpler post list than Bear Blog’s date-prefixed flex rows.

## Decision
Customize the site **via project overlays** (do not fork the theme):

1. **Homepage list** — `site/layouts/index.html` paginates `Section == "blog"` with Hugo’s built-in `.Paginate` / `.Paginator` (`[pagination] pagerSize = 10` in `hugo.toml`).
2. **List chrome** — titles only, HTML disc bullets (`ul.home-posts`); no dates on the homepage list. `/blog/` keeps the theme’s dated list.
3. **Pagination chrome** — custom `site/layouts/partials/pagination.html` renders an **inline** trail with middle-dot `·` separators (not Hugo’s default bulleted `_internal/pagination.html` list).
4. **Typography** — self-host [Outfit](https://fonts.google.com/specimen/Outfit) latin woff2 (weights 400, 600, 700) under `site/static/fonts/`, declare `@font-face` + preload 400 in `custom_head.html`, and set Bear Blog CSS variables `--font-main` / `--font-secondary` to Outfit. Do not load Google Fonts CDN.

## Alternatives Considered

### Keep Bear Blog homepage content-only; rely on `/blog/` for the index
- Pros: Zero custom layouts
- Cons: Weak first-viewport experience vs the old WP home
- Rejected: Homepage should list recent posts

### Use stock `_internal/pagination.html`
- Pros: Zero custom partial
- Cons: Default markup is a vertical/`ul` page list that fought the minimal inline look
- Rejected: Inline `·` separators preferred

### Google Fonts CDN for Outfit
- Pros: Zero binary assets in git; easy weight changes
- Cons: Render-blocking CSS + critical chain to `fonts.gstatic.com`; hurts LCP/PageSpeed
- Rejected: Self-hosted Outfit woff2 under `/fonts/` (see `docs/superpowers/specs/2026-07-31-pagespeed-fonts-ga-design.md`)

### Keep Verdana / system stack only
- Pros: Best possible font-related PageSpeed; no font files
- Cons: Weaker brand type vs Outfit
- Rejected: Outfit retained; delivery method changed to self-host

### Put dates back on the homepage list
- Pros: Matches `/blog/` and Bear Blog defaults
- Cons: Conflicts with the requested bullet-only list
- Rejected: Explicit UX choice

## Consequences
- Presentation changes live under `site/layouts/` and `custom_head.html`; theme submodule stays stock
- Homepage pagination URLs are `/page/N/` under the Hugo `pagination.path`
- Outfit woff2 files are same-origin static assets under `/fonts/` (fallback: Verdana in the font stack); no Google Fonts CDN at runtime
- GA4 `G-60P3WJPWMJ` is injected after `window` `load` (presentation/perf detail; measurement ID unchanged)
- Changing separator, page size, or typeface does not require a new ADR unless the *policy* changes (e.g. force dark mode, abandon pagination)
