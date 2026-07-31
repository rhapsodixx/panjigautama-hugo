# PageSpeed: Self-host Outfit + Defer GA4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove Google Fonts CDN and defer GA4 gtag until after `window` `load` so mobile Lighthouse/PageSpeed on the homepage can reach 100 on all four categories (max three measure→fix loops).

**Architecture:** Vendor latin Outfit woff2 (400/600/700) under `site/static/fonts/`, declare them with `@font-face` + preload 400 in `custom_head.html`, and replace the eager gtag `<script src>` with an inline loader that injects gtag only on `load`. Amend ADR-006 to match. Verify with Hugo build smoke checks, then Lighthouse/PageSpeed (prefer production after deploy).

**Tech Stack:** Hugo, hugo-bearblog overlays, static woff2 (fontsource Outfit 5.2.5), GA4 `G-60P3WJPWMJ`, Lighthouse CLI / PageSpeed Insights

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-31-pagespeed-fonts-ga-design.md`
- Measurement ID exactly: `G-60P3WJPWMJ`
- Outfit weights only: **400**, **600**, **700** (latin subset)
- Font files: `site/static/fonts/outfit-latin-{400,600,700}.woff2` plus `site/static/fonts/OFL.txt`
- Preload weight **400** only on attempt 1
- No Google Fonts CDN (`fonts.googleapis.com` / `fonts.gstatic.com`) after Task 2
- No eager `gtag/js` script tag in initial HTML after Task 2
- Do not fork `site/themes/hugo-bearblog`
- Cap: **3** measure→fix→remeasure attempts; stop and report residuals after attempt 3
- Font source pin: `@fontsource/outfit@5.2.5` via jsDelivr (reproducible)

---

## File map

| File | Responsibility |
|------|----------------|
| `site/static/fonts/outfit-latin-400.woff2` | Self-hosted Outfit regular |
| `site/static/fonts/outfit-latin-600.woff2` | Self-hosted Outfit semi-bold (pagination current) |
| `site/static/fonts/outfit-latin-700.woff2` | Self-hosted Outfit bold |
| `site/static/fonts/OFL.txt` | SIL OFL 1.1 license for Outfit |
| `site/layouts/partials/custom_head.html` | `@font-face`, preload 400, deferred GA, existing homepage CSS |
| `docs/decisions/ADR-006-homepage-presentation.md` | Typography policy: self-hosted Outfit |
| `docs/qa-checklist.md` | Optional note that GA is deferred (only if historical rows stay intact) |

**Unchanged:** theme submodule, Dockerfile, Compose, Caddy, content Markdown, homepage/pagination layouts.

---

### Task 1: Vendor Outfit fonts + OFL

**Files:**
- Create: `site/static/fonts/outfit-latin-400.woff2`
- Create: `site/static/fonts/outfit-latin-600.woff2`
- Create: `site/static/fonts/outfit-latin-700.woff2`
- Create: `site/static/fonts/OFL.txt`

**Interfaces:**
- Consumes: jsDelivr fontsource URLs for Outfit 5.2.5 latin normals
- Produces: same-origin paths `/fonts/outfit-latin-400.woff2`, `/fonts/outfit-latin-600.woff2`, `/fonts/outfit-latin-700.woff2`, `/fonts/OFL.txt`

- [ ] **Step 1: Create directory and download woff2 files**

Run from repo root:

```bash
mkdir -p site/static/fonts
curl -fsSL -o site/static/fonts/outfit-latin-400.woff2 \
  "https://cdn.jsdelivr.net/fontsource/fonts/outfit@5.2.5/latin-400-normal.woff2"
curl -fsSL -o site/static/fonts/outfit-latin-600.woff2 \
  "https://cdn.jsdelivr.net/fontsource/fonts/outfit@5.2.5/latin-600-normal.woff2"
curl -fsSL -o site/static/fonts/outfit-latin-700.woff2 \
  "https://cdn.jsdelivr.net/fontsource/fonts/outfit@5.2.5/latin-700-normal.woff2"
```

Expected: three files; each roughly 10–20 KiB; `file` reports `Web Open Font Format`.

- [ ] **Step 2: Verify files are real woff2 (not HTML error pages)**

Run:

```bash
ls -la site/static/fonts/*.woff2
file site/static/fonts/outfit-latin-400.woff2
xxd -l 4 site/static/fonts/outfit-latin-400.woff2
```

Expected: sizes > 5 KiB each; `file` mentions woff2 / OpenType; first bytes are `wOF2` (`77 4f 46 32`).

- [ ] **Step 3: Download OFL license text**

Run:

```bash
curl -fsSL -o site/static/fonts/OFL.txt \
  "https://cdn.jsdelivr.net/npm/@fontsource/outfit@5.2.5/LICENSE"
head -5 site/static/fonts/OFL.txt
```

Expected: file mentions `SIL Open Font License`.

- [ ] **Step 4: Commit**

```bash
git add site/static/fonts/
git commit -m "$(cat <<'EOF'
chore: vendor Outfit latin woff2 fonts under static/fonts

EOF
)"
```

---

### Task 2: Self-host fonts + defer GA in `custom_head.html`

**Files:**
- Modify: `site/layouts/partials/custom_head.html` (replace entire file)

**Interfaces:**
- Consumes: `/fonts/outfit-latin-{400,600,700}.woff2` from Task 1
- Produces: HTML with preload + `@font-face`; deferred GA injector; no Google Fonts CDN; no eager `gtag/js` tag

- [ ] **Step 1: Replace `site/layouts/partials/custom_head.html` with:**

```html
<link rel="preload" href="/fonts/outfit-latin-400.woff2" as="font" type="font/woff2" crossorigin>
<!-- Google Analytics GA4 (deferred until window load) -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  window.addEventListener('load', function () {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-60P3WJPWMJ';
    s.onload = function () {
      gtag('js', new Date());
      gtag('config', 'G-60P3WJPWMJ');
    };
    document.head.appendChild(s);
  });
</script>
<style>
  @font-face {
    font-family: "Outfit";
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url("/fonts/outfit-latin-400.woff2") format("woff2");
  }
  @font-face {
    font-family: "Outfit";
    font-style: normal;
    font-weight: 600;
    font-display: swap;
    src: url("/fonts/outfit-latin-600.woff2") format("woff2");
  }
  @font-face {
    font-family: "Outfit";
    font-style: normal;
    font-weight: 700;
    font-display: swap;
    src: url("/fonts/outfit-latin-700.woff2") format("woff2");
  }

  :root {
    --font-main: "Outfit", Verdana, sans-serif;
    --font-secondary: "Outfit", Verdana, sans-serif;
  }

  /* Homepage post list: bullets, no dates */
  ul.home-posts {
    list-style-type: disc;
    padding-left: 1.25em;
    margin: 1em 0 0;
  }
  ul.home-posts li {
    display: list-item;
    margin: 0.35em 0;
  }

  /* Inline pagination: · separators, no list bullets */
  .pagination {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0;
    margin: 1.5em 0 0;
    padding: 0;
    list-style: none;
    font-size: 15px;
    line-height: 1.5;
  }
  .pagination a,
  .pagination .pagination-current {
    padding: 0.15em 0.1em;
  }
  .pagination-sep {
    margin: 0 0.45em;
    color: var(--text-color);
    opacity: 0.45;
    user-select: none;
  }
  .pagination-current {
    font-weight: 600;
    color: var(--heading-color);
  }
</style>
```

- [ ] **Step 2: Build Hugo and smoke-check HTML**

Run from repo root (site lives under `site/`):

```bash
cd site && hugo --minify -d ../public-check && cd ..
rg -n 'fonts\.googleapis|fonts\.gstatic|gtag/js' public-check/index.html || true
rg -n 'outfit-latin-400|@font-face|G-60P3WJPWMJ|addEventListener\(.load' public-check/index.html
test -f public-check/fonts/outfit-latin-400.woff2
test -f public-check/fonts/outfit-latin-600.woff2
test -f public-check/fonts/outfit-latin-700.woff2
```

Expected:
- First `rg` finds **no** `fonts.googleapis` / `fonts.gstatic` and **no** literal `src=...gtag/js` (string `gtag/js` may appear only inside the deferred loader’s `s.src = '...'` assignment — that is OK).
- Second `rg` finds `@font-face`, `outfit-latin-400`, `G-60P3WJPWMJ`, and `load` listener.
- All three `test -f` succeed.

Stricter check that there is no eager script tag:

```bash
rg -n '<script[^>]+gtag/js' public-check/index.html || echo "OK: no eager gtag script tag"
```

Expected: `OK: no eager gtag script tag`

- [ ] **Step 3: Serve locally and confirm font bytes**

Run:

```bash
cd site && hugo server --bind 127.0.0.1 --port 1313
```

In another shell:

```bash
curl -sI http://127.0.0.1:1313/fonts/outfit-latin-400.woff2 | head -5
curl -s http://127.0.0.1:1313/ | rg -o 'fonts\.googleapis|outfit-latin-400|G-60P3WJPWMJ' | sort -u
```

Expected: `200` for woff2; homepage HTML mentions `outfit-latin-400` and `G-60P3WJPWMJ`, not `fonts.googleapis`.

Stop the server when done (`Ctrl-C`).

- [ ] **Step 4: Commit**

```bash
git add site/layouts/partials/custom_head.html
git commit -m "$(cat <<'EOF'
perf: self-host Outfit and defer GA4 until window load

EOF
)"
```

Cleanup build dir if desired: `rm -rf public-check`

---

### Task 3: Amend ADR-006 for self-hosted Outfit

**Files:**
- Modify: `docs/decisions/ADR-006-homepage-presentation.md`

**Interfaces:**
- Consumes: decisions from the design spec (self-host 400/600/700; no Google Fonts CDN)
- Produces: ADR text that matches production behavior after Task 2

- [ ] **Step 1: Update typography decision bullet**

In `docs/decisions/ADR-006-homepage-presentation.md`, change decision item 4 from Google Fonts CDN to self-hosted fonts. Replace that numbered item with:

```markdown
4. **Typography** — self-host [Outfit](https://fonts.google.com/specimen/Outfit) latin woff2 (weights 400, 600, 700) under `site/static/fonts/`, declare `@font-face` + preload 400 in `custom_head.html`, and set Bear Blog CSS variables `--font-main` / `--font-secondary` to Outfit. Do not load Google Fonts CDN.
```

- [ ] **Step 2: Replace the rejected “Self-host Outfit” alternative**

Replace the subsection:

```markdown
### Self-host Outfit or keep Verdana
- Pros: No Google Fonts request; theme default
- Cons: Weaker brand type; self-host adds asset ops
- Rejected: Outfit via Google Fonts accepted for v1
```

with:

```markdown
### Google Fonts CDN for Outfit
- Pros: Zero binary assets in git; easy weight changes
- Cons: Render-blocking CSS + critical chain to `fonts.gstatic.com`; hurts LCP/PageSpeed
- Rejected: Self-hosted Outfit woff2 under `/fonts/` (see `docs/superpowers/specs/2026-07-31-pagespeed-fonts-ga-design.md`)

### Keep Verdana / system stack only
- Pros: Best possible font-related PageSpeed; no font files
- Cons: Weaker brand type vs Outfit
- Rejected: Outfit retained; delivery method changed to self-host
```

- [ ] **Step 3: Update Consequences**

Replace the Google Fonts consequence bullet:

```markdown
- Google Fonts is a runtime dependency for typography (fallback: Verdana in the font stack)
```

with:

```markdown
- Outfit woff2 files are same-origin static assets under `/fonts/` (fallback: Verdana in the font stack); no Google Fonts CDN at runtime
- GA4 `G-60P3WJPWMJ` is injected after `window` `load` (presentation/perf detail; measurement ID unchanged)
```

- [ ] **Step 4: Commit**

```bash
git add docs/decisions/ADR-006-homepage-presentation.md
git commit -m "$(cat <<'EOF'
docs: amend ADR-006 for self-hosted Outfit typography

EOF
)"
```

---

### Task 4: Attempt 1 — local Lighthouse, then production measure

**Files:**
- None required (measurement only). If production is behind, push/deploy existing commits first.

**Interfaces:**
- Consumes: Tasks 1–3 on the measured URL
- Produces: Attempt-1 score log (all four categories); decide whether Task 5/6 needed

- [ ] **Step 1: Local Lighthouse (optional early loop)**

With `hugo server` on `1313` (or Docker Compose on network `web`), run:

```bash
npx --yes lighthouse http://127.0.0.1:1313/ \
  --only-categories=performance,accessibility,best-practices,seo \
  --form-factor=mobile \
  --screenEmulation.mobile=true \
  --output=json \
  --output-path=./lighthouse-attempt1-local.json \
  --quiet \
  --chrome-flags="--headless --no-sandbox"
node -e "const r=require('./lighthouse-attempt1-local.json'); const c=r.categories; for (const k of Object.keys(c)) console.log(k, Math.round(c[k].score*100));"
```

Expected: note scores. Localhost scores can differ from PSI production; still useful for catching regressions.

- [ ] **Step 2: Deploy to production**

Push commits to `main` (triggers deploy Action) **or** run `scripts/deploy.sh` if that is the operator path. Wait until `https://panjigautama.com/` HTML shows self-hosted fonts:

```bash
curl -s https://panjigautama.com/ | rg -n 'fonts\.googleapis|outfit-latin-400|addEventListener' | head
curl -sI https://panjigautama.com/fonts/outfit-latin-400.woff2 | head -5
```

Expected: no `fonts.googleapis`; `outfit-latin-400` present; woff2 returns `200`.

- [ ] **Step 3: PageSpeed Insights / Lighthouse against production (Attempt 1)**

Run mobile Lighthouse against production:

```bash
npx --yes lighthouse https://panjigautama.com/ \
  --only-categories=performance,accessibility,best-practices,seo \
  --form-factor=mobile \
  --screenEmulation.mobile=true \
  --output=json \
  --output-path=./lighthouse-attempt1-prod.json \
  --quiet \
  --chrome-flags="--headless --no-sandbox"
node -e "const r=require('./lighthouse-attempt1-prod.json'); const c=r.categories; for (const k of Object.keys(c)) console.log(k, Math.round(c[k].score*100)); const audits=['render-blocking-resources','critical-request-chains','unused-javascript']; for (const a of audits) { const x=r.audits[a]; console.log(a, x.score, x.displayValue||''); }"
```

Record:

| Category | Score |
|----------|-------|
| performance | |
| accessibility | |
| best-practices | |
| seo | |

- [ ] **Step 4: Gate**

- If **all four are 100**: skip Tasks 5–6; commit any score notes only if the operator wants them in docs; done.
- If not: proceed to Task 5 (Attempt 2). Do **not** start Attempt 2 without recording Attempt 1 scores.

Do not commit `lighthouse-*.json` unless explicitly requested (add to `.gitignore` locally or delete after reading).

---

### Task 5: Attempt 2 — stronger GA deferral and/or drop font preload

**Files:**
- Modify: `site/layouts/partials/custom_head.html` (only if Attempt 1 failed)

**Interfaces:**
- Consumes: Attempt 1 residual audits
- Produces: Attempt 2 HTML behavior per design retry ladder

Apply **only the fixes matching the failing audits**:

**If unused-javascript / Performance still hurt by gtag:** replace the `load` listener block with idle + timeout deferral:

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  function loadGtag() {
    if (window.__gtagLoaded) return;
    window.__gtagLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-60P3WJPWMJ';
    s.onload = function () {
      gtag('js', new Date());
      gtag('config', 'G-60P3WJPWMJ');
    };
    document.head.appendChild(s);
  }
  function scheduleGtag() {
    if ('requestIdleCallback' in window) {
      requestIdleCallback(loadGtag, { timeout: 3000 });
    } else {
      setTimeout(loadGtag, 2000);
    }
  }
  window.addEventListener('load', scheduleGtag);
</script>
```

**If render-blocking / LCP still flags font preload:** remove this line from `custom_head.html`:

```html
<link rel="preload" href="/fonts/outfit-latin-400.woff2" as="font" type="font/woff2" crossorigin>
```

- [ ] **Step 1: Apply the matching change(s) above**

- [ ] **Step 2: Rebuild smoke**

```bash
cd site && hugo --minify -d ../public-check && cd ..
rg -n '<script[^>]+gtag/js|fonts\.googleapis' public-check/index.html || echo "OK"
rg -n 'requestIdleCallback|outfit-latin-400' public-check/index.html
```

- [ ] **Step 3: Commit**

```bash
git add site/layouts/partials/custom_head.html
git commit -m "$(cat <<'EOF'
perf: strengthen deferred GA / adjust font preload for Lighthouse

EOF
)"
```

- [ ] **Step 4: Deploy and remeasure (Attempt 2)**

Same production curl + lighthouse commands as Task 4 Steps 2–3, writing `lighthouse-attempt2-prod.json`. Record scores. If all 100, stop. Else Task 6.

---

### Task 6: Attempt 3 — last high-impact leftovers, then stop

**Files:**
- Modify: `site/layouts/partials/custom_head.html` and/or font set **only** for residuals that still fit the spec

**Interfaces:**
- Consumes: Attempt 2 residuals
- Produces: Final Attempt 3 scores or residual report

Allowed Attempt 3 levers (pick only what audits demand):

1. **First-interaction GA:** also call `loadGtag` on first `pointerdown` / `keydown` (in addition to idle), still never eager in head.
2. **Drop weight 600 file** only if audits show it unused and pagination can use `font-weight: 700` instead — update `@font-face`, CSS `.pagination-current { font-weight: 700; }`, and remove `outfit-latin-600.woff2` from static + commit.
3. Do **not** remove GA, add Partytown, or redesign the homepage.

- [ ] **Step 1: Implement the chosen Attempt 3 change**

- [ ] **Step 2: Smoke + commit + deploy**

Same patterns as Task 5.

- [ ] **Step 3: Remeasure (Attempt 3)**

Write `lighthouse-attempt3-prod.json` and record all four scores.

- [ ] **Step 4: Final report**

If all 100: done. If not: stop. Report remaining audits (id, title, savings) from the JSON — do not start a fourth loop.

```bash
node -e "const r=require('./lighthouse-attempt3-prod.json'); const c=r.categories; for (const k of Object.keys(c)) console.log(k, Math.round(c[k].score*100)); Object.values(r.audits).filter(a=>a.score!==null&&a.score<1&&a.details).slice(0,15).forEach(a=>console.log(a.id, a.title, a.displayValue||''));"
```

---

## Spec coverage (self-review)

| Spec requirement | Task |
|------------------|------|
| Self-host Outfit 400/600/700 + OFL | Task 1 |
| `@font-face`, preload 400, remove Google Fonts CDN | Task 2 |
| Defer GA until `window` `load` | Task 2 |
| Amend ADR-006 | Task 3 |
| Build smoke / visual unchanged layouts | Task 2 (+ layouts untouched) |
| Measure loop, max 3 attempts | Tasks 4–6 |
| Attempt 2 idle/preload ladder | Task 5 |
| Attempt 3 leftovers then stop | Task 6 |
