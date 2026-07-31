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
4. **Typography** — load [Outfit](https://fonts.google.com/specimen/Outfit) from Google Fonts in `custom_head.html` and set Bear Blog CSS variables `--font-main` / `--font-secondary` to Outfit.

## Alternatives Considered

### Keep Bear Blog homepage content-only; rely on `/blog/` for the index
- Pros: Zero custom layouts
- Cons: Weak first-viewport experience vs the old WP home
- Rejected: Homepage should list recent posts

### Use stock `_internal/pagination.html`
- Pros: Zero custom partial
- Cons: Default markup is a vertical/`ul` page list that fought the minimal inline look
- Rejected: Inline `·` separators preferred

### Self-host Outfit or keep Verdana
- Pros: No Google Fonts request; theme default
- Cons: Weaker brand type; self-host adds asset ops
- Rejected: Outfit via Google Fonts accepted for v1

### Put dates back on the homepage list
- Pros: Matches `/blog/` and Bear Blog defaults
- Cons: Conflicts with the requested bullet-only list
- Rejected: Explicit UX choice

## Consequences
- Presentation changes live under `site/layouts/` and `custom_head.html`; theme submodule stays stock
- Homepage pagination URLs are `/page/N/` under the Hugo `pagination.path`
- Google Fonts is a runtime dependency for typography (fallback: Verdana in the font stack)
- Changing separator, page size, or typeface does not require a new ADR unless the *policy* changes (e.g. force dark mode, abandon pagination)
