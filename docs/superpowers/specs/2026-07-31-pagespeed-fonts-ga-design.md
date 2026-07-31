# PageSpeed: self-host Outfit + defer GA4

**Date:** 2026-07-31  
**Status:** Approved  
**Repo:** `panjigautama-hugo`  
**Related:** [ADR-006](../../decisions/ADR-006-homepage-presentation.md), PageSpeed findings on `https://panjigautama.com/` (Performance ~91)

## Goal

Raise mobile PageSpeed Insights / Lighthouse category scores on the homepage toward **100** for Performance, Accessibility, Best Practices, and SEO. Cap the work at **three** measure → fix → remeasure loops. Stop and report residuals if all-100s is not reached by attempt three.

## Problem

PageSpeed flagged three issues on the live homepage:

1. **Render-blocking Google Fonts CSS** (`fonts.googleapis.com` Outfit stylesheet) delaying FCP/LCP.
2. **Critical request chain** — document → Google Fonts CSS → `fonts.gstatic.com` woff2.
3. **Unused JavaScript** — early `gtag/js` for GA4 `G-60P3WJPWMJ` (~146 KiB transfer, ~66 KiB estimated savings).

These come from `site/layouts/partials/custom_head.html` (Google Fonts links + eager gtag). ADR-006 previously accepted Outfit via Google Fonts CDN and rejected self-hosting for v1.

## Decisions

| Topic | Choice |
|-------|--------|
| Fonts | Self-host Outfit woff2 (weights **400**, **600**, **700**) under `site/static/fonts/` |
| Font loading | `@font-face` with `font-display: swap`; preload weight **400** only on attempt 1; remove all `fonts.googleapis.com` / `fonts.gstatic.com` links |
| Analytics | Keep GA4 `G-60P3WJPWMJ`; inject `gtag/js` only after `window` `load` |
| Theme | Project overlays only; do not fork hugo-bearblog |
| Approach | Minimal overlay (commit font binaries + edit `custom_head.html`); no build-time font fetch script; no Partytown |

## Out of scope

- Removing analytics
- Partytown or other worker proxies
- Image / caching-header / Caddy changes unless a remeasure within the three attempts still blocks all-100s
- Changing homepage layout, bullets, or pagination chrome

## Architecture

```text
Browser
  │
  ├─ HTML head (custom_head.html)
  │    ├─ preload /fonts/outfit-latin-400.woff2
  │    ├─ <style> @font-face ×3 + existing site CSS vars
  │    └─ inline deferred GA loader (registers on window "load")
  │
  ├─ Same-origin GET /fonts/outfit-*.woff2
  │
  └─ After load → inject googletagmanager gtag/js + gtag('config', …)
```

### Components

| Path | Role |
|------|------|
| `site/static/fonts/outfit-latin-{400,600,700}.woff2` | Outfit latin subsets for 400, 600, 700 |
| `site/static/fonts/OFL.txt` | Outfit OFL license notice |
| `site/layouts/partials/custom_head.html` | `@font-face`, preload, deferred GA; no Google Fonts CDN |
| `docs/decisions/ADR-006-homepage-presentation.md` | Update typography decision: self-hosted Outfit replaces Google Fonts CDN |

### Deferred GA loader (behavior)

1. Define `dataLayer` / `gtag` stub inline (or create them when injecting).
2. On `window` `load`, dynamically insert `<script async src="https://www.googletagmanager.com/gtag/js?id=G-60P3WJPWMJ">` and call `gtag('config', 'G-60P3WJPWMJ')`.
3. Do not place an eager `src=…/gtag/js` in the initial head markup.

### Font stack

Keep `--font-main` / `--font-secondary` as `"Outfit", Verdana, sans-serif` so missing or slow fonts fall back to Verdana.

## Retry ladder (within 3 attempts)

If scores are not all 100 after the baseline change:

1. **Attempt 2:** Stronger GA deferral (`requestIdleCallback` with timeout, and/or first interaction) if unused-JS still hurts Performance; adjust font preload (drop or keep only 400) if LCP/chain still flags.
2. **Attempt 3:** Only remaining high-impact leftovers that still fit this spec’s spirit (e.g. further subsetting). Do not expand into unrelated site redesign.

## Verification

1. **Build smoke:** Hugo output HTML contains `/fonts/` and `@font-face`; contains no `fonts.googleapis.com` / `fonts.gstatic.com`; initial HTML has no eager `gtag/js` script tag (only the deferred injector).
2. **Visual:** Homepage still renders Outfit; bullets and pagination unchanged.
3. **Score:** PageSpeed Insights (mobile) and/or `npx lighthouse` against the measured URL (prefer production after deploy; local serve acceptable for early loops). Record all four category scores each attempt.
4. **Success:** All four categories at 100, or a residual audit report after three attempts.

## Consequences

- Outfit becomes a same-origin static asset; typography no longer depends on Google Fonts at runtime.
- GA4 still runs for real users after load; Lighthouse may not count gtag in the critical window if deferral is late enough.
- Font binaries are committed in git (~tens of KiB each); upgrades mean replacing files manually.
- ADR-006 must be amended so self-hosting is policy, not a rejected alternative.
