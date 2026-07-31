# WordPress → Hugo Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate panjigautama.com from WordPress to a Hugo + hugo-bearblog static site with root-level URLs, `/images/` media, GA4, favicon, and Docker Compose deploy behind host Caddy.

**Architecture:** A Python WXR converter turns `wordpress-backup/*.xml` into Markdown under `site/content/` and downloads media into `site/static/images/` while rewriting URLs. Hugo builds with Bear Blog; a multi-stage Docker image serves `public/` on `:8080` for host Caddy to reverse-proxy.

**Tech Stack:** Hugo (extended), hugo-bearblog (git submodule), Python 3.11+ (`html2text`), Docker + Compose, host Caddy, GA4 `G-60P3WJPWMJ`

## Global Constraints

- Public post/page URLs must be root-level: `/<slug>/` (ADR-002)
- Media lives under `/images/`; rewrite in-content refs; **no** `/wp-content/` redirects (ADR-003)
- Comments out of scope for v1
- Theme: hugo-bearblog, light default (system dark via CSS is OK)
- GA measurement ID exactly: `G-60P3WJPWMJ`
- Favicon sourced from live panjigautama.com
- Compose builds Hugo on VPS; host Caddy owns TLS (ADR-004)
- Migrate only **published** posts/pages (45 posts, 3 pages); skip drafts and `inherit` stubs
- Do not disable Hugo taxonomies — categories must have term pages (overrides Bear Blog exampleSite’s `disableKinds = ["taxonomy"]`)
- Already done (do not redo): public repo `panjigautama-hugo`, `AGENTS.md`, `CLAUDE.md`, ADRs, design spec, WXR backups committed

---

## File structure (target)

| Path | Responsibility |
|------|----------------|
| `site/hugo.toml` | Site config, theme, root permalinks, taxonomies, favicon param |
| `site/content/_index.md` | Homepage body |
| `site/content/blog/_index.md` | Blog list page (`/blog/`) |
| `site/content/blog/<slug>.md` | Migrated posts (URL `/<slug>/` via permalinks) |
| `site/content/<slug>.md` | Migrated pages |
| `site/static/images/*` | Migrated media |
| `site/static/images/favicon.png` | Site favicon (Bear Blog `params.favicon`) |
| `site/static/favicon.ico` | Optional browser default |
| `site/layouts/partials/custom_head.html` | GA4 gtag snippet |
| `site/themes/hugo-bearblog/` | Theme submodule |
| `scripts/wxr_migrate/` | Converter package |
| `scripts/wxr_migrate/parse.py` | Parse WXR → dataclasses |
| `scripts/wxr_migrate/rewrite.py` | URL rewrite helpers |
| `scripts/wxr_migrate/media.py` | Download media + collision names |
| `scripts/wxr_migrate/write.py` | Emit Markdown files |
| `scripts/wxr_migrate/__main__.py` | CLI entry |
| `scripts/requirements.txt` | `html2text` |
| `scripts/tests/` | Pytest fixtures + unit tests |
| `Dockerfile` | Multi-stage Hugo build → static serve |
| `docker-compose.yml` | `blog` service |
| `Caddyfile.snippet` | Host Caddy reverse-proxy example |
| `docs/operations-cutover.md` | VPS cutover + rollback runbook |

---

### Task 1: Scaffold Hugo site + Bear Blog theme + config

**Files:**
- Create: `site/hugo.toml`
- Create: `site/content/_index.md`
- Create: `site/content/blog/_index.md`
- Create: `site/layouts/partials/custom_head.html` (empty stub OK)
- Modify: `.gitignore` (ensure `site/public/` ignored — already present)
- Create: `site/themes/hugo-bearblog` via git submodule

**Interfaces:**
- Consumes: none
- Produces: runnable empty Hugo site at `site/` with `theme = 'hugo-bearblog'`, permalinks `blog = "/:slug/"`, taxonomies enabled

- [ ] **Step 1: Verify Hugo is installed**

Run: `hugo version`
Expected: version string containing `hugo` (v0.120+ preferred; extended edition OK)

If missing: `brew install hugo`

- [ ] **Step 2: Add theme submodule**

```bash
cd /Users/panji.gautama/Documents/Project/panjigautamacom-blog
mkdir -p site
git submodule add https://github.com/janraasch/hugo-bearblog.git site/themes/hugo-bearblog
```

Expected: `site/themes/hugo-bearblog/theme.toml` exists

- [ ] **Step 3: Write `site/hugo.toml`**

```toml
baseURL = "https://panjigautama.com"
theme = "hugo-bearblog"
title = "Panji Gautama"
author = "Panji Gautama"
copyright = "Copyright © Panji Gautama"
languageCode = "en-US"
enableRobotsTXT = true

# Keep taxonomies enabled (do NOT copy Bear Blog exampleSite disableKinds)
[taxonomies]
  category = "categories"
  tag = "tags"

[permalinks]
  blog = "/:slug/"
  categories = "/categories/:slug/"
  tags = "/tags/:slug/"

[params]
  description = "Notes on engineering, product, and personal growth."
  favicon = "images/favicon.png"
  title = "Panji Gautama"
  enablePostNavigator = true

[markup]
  [markup.highlight]
    style = "friendly"
    lineNos = true
    lineNumbersInTable = false
    codeFences = true
```

- [ ] **Step 4: Add minimal content so Hugo builds**

`site/content/_index.md`:

```markdown
---
title: "Home"
---

Welcome to my blog.
```

`site/content/blog/_index.md`:

```markdown
---
title: "Blog"
---
```

`site/layouts/partials/custom_head.html`:

```html
<!-- GA and extra head tags added in Task 5 -->
```

- [ ] **Step 5: Build locally to verify scaffold**

Run: `cd site && hugo --minify`
Expected: `Total in ...` with exit code 0; `site/public/index.html` exists

- [ ] **Step 6: Commit**

```bash
git add .gitmodules site/themes/hugo-bearblog site/hugo.toml site/content site/layouts
git commit -m "$(cat <<'EOF'
feat: scaffold Hugo site with hugo-bearblog theme

Add base config with root-level blog permalinks and enabled
category taxonomies for the WordPress migration.
EOF
)"
```

---

### Task 2: WXR parser + URL rewrite helpers (TDD)

**Files:**
- Create: `scripts/requirements.txt`
- Create: `scripts/wxr_migrate/__init__.py`
- Create: `scripts/wxr_migrate/parse.py`
- Create: `scripts/wxr_migrate/rewrite.py`
- Create: `scripts/tests/fixtures/mini-posts.xml`
- Create: `scripts/tests/test_parse.py`
- Create: `scripts/tests/test_rewrite.py`

**Interfaces:**
- Consumes: WXR XML files
- Produces:
  - `dataclass ContentItem(title: str, slug: str, date: str, lastmod: str, status: str, post_type: str, categories: list[str], tags: list[str], content_html: str)`
  - `parse_wxr(path: Path) -> list[ContentItem]` — returns all items; caller filters `status == "publish"` and `post_type in {"post","page"}`
  - `rewrite_media_urls(html: str, url_map: dict[str, str]) -> str` — replaces absolute and root-relative WP upload URLs using `url_map` keys (old URL or path) → values (`/images/filename`)

- [ ] **Step 1: Add dependencies and empty package**

`scripts/requirements.txt`:

```text
html2text==2024.2.26
pytest==8.3.5
```

```bash
cd scripts && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Create empty `scripts/wxr_migrate/__init__.py`

- [ ] **Step 2: Write failing parser test + fixture**

`scripts/tests/fixtures/mini-posts.xml`:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:wp="http://wordpress.org/export/1.2/">
  <channel>
    <item>
      <title><![CDATA[Hello World]]></title>
      <content:encoded><![CDATA[<p>Hi <img src="https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png" /></p>]]></content:encoded>
      <wp:post_name><![CDATA[hello-world]]></wp:post_name>
      <wp:post_type><![CDATA[post]]></wp:post_type>
      <wp:status><![CDATA[publish]]></wp:status>
      <wp:post_date><![CDATA[2021-01-15 10:00:00]]></wp:post_date>
      <wp:post_modified><![CDATA[2021-01-16 11:00:00]]></wp:post_modified>
      <category domain="category" nicename="management"><![CDATA[Management]]></category>
      <category domain="post_tag" nicename="notes"><![CDATA[notes]]></category>
    </item>
    <item>
      <title><![CDATA[Drafty]]></title>
      <content:encoded><![CDATA[<p>nope</p>]]></content:encoded>
      <wp:post_name><![CDATA[drafty]]></wp:post_name>
      <wp:post_type><![CDATA[post]]></wp:post_type>
      <wp:status><![CDATA[draft]]></wp:status>
      <wp:post_date><![CDATA[2021-02-01 10:00:00]]></wp:post_date>
      <wp:post_modified><![CDATA[2021-02-01 10:00:00]]></wp:post_modified>
    </item>
  </channel>
</rss>
```

`scripts/tests/test_parse.py`:

```python
from pathlib import Path
from wxr_migrate.parse import parse_wxr

FIXTURE = Path(__file__).parent / "fixtures" / "mini-posts.xml"


def test_parse_wxr_reads_published_and_draft():
    items = parse_wxr(FIXTURE)
    assert len(items) == 2
    published = [i for i in items if i.status == "publish"]
    assert len(published) == 1
    post = published[0]
    assert post.title == "Hello World"
    assert post.slug == "hello-world"
    assert post.post_type == "post"
    assert post.categories == ["Management"]
    assert post.tags == ["notes"]
    assert "vue-1.png" in post.content_html
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd scripts && source .venv/bin/activate && PYTHONPATH=. pytest tests/test_parse.py -v`
Expected: FAIL (import error or missing `parse_wxr`)

- [ ] **Step 4: Implement `parse.py`**

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import xml.etree.ElementTree as ET

NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


@dataclass
class ContentItem:
    title: str
    slug: str
    date: str
    lastmod: str
    status: str
    post_type: str
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    content_html: str = ""


def _text(el: ET.Element | None) -> str:
    if el is None or el.text is None:
        return ""
    return el.text.strip()


def parse_wxr(path: Path) -> list[ContentItem]:
    tree = ET.parse(path)
    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        raise ValueError(f"No channel in {path}")

    items: list[ContentItem] = []
    for item in channel.findall("item"):
        title = _text(item.find("title"))
        slug = _text(item.find("wp:post_name", NS))
        status = _text(item.find("wp:status", NS))
        post_type = _text(item.find("wp:post_type", NS))
        date = _text(item.find("wp:post_date", NS))
        lastmod = _text(item.find("wp:post_modified", NS)) or date
        content_html = _text(item.find("content:encoded", NS))

        categories: list[str] = []
        tags: list[str] = []
        for cat in item.findall("category"):
            domain = cat.attrib.get("domain", "")
            label = (cat.text or "").strip()
            if not label:
                continue
            if domain == "category":
                categories.append(label)
            elif domain == "post_tag":
                tags.append(label)

        items.append(
            ContentItem(
                title=title,
                slug=slug,
                date=date,
                lastmod=lastmod,
                status=status,
                post_type=post_type,
                categories=categories,
                tags=tags,
                content_html=content_html,
            )
        )
    return items
```

- [ ] **Step 5: Run parser test — expect PASS**

Run: `cd scripts && source .venv/bin/activate && PYTHONPATH=. pytest tests/test_parse.py -v`
Expected: PASS

- [ ] **Step 6: Write failing rewrite test**

`scripts/tests/test_rewrite.py`:

```python
from wxr_migrate.rewrite import rewrite_media_urls


def test_rewrite_absolute_and_relative_upload_urls():
    html = (
        '<img src="https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png" />'
        '<img src="/wp-content/uploads/2021/01/vue-2.png" />'
    )
    url_map = {
        "https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png": "/images/vue-1.png",
        "https://panjigautama.com/wp-content/uploads/2021/01/vue-2.png": "/images/vue-2.png",
        "/wp-content/uploads/2021/01/vue-1.png": "/images/vue-1.png",
        "/wp-content/uploads/2021/01/vue-2.png": "/images/vue-2.png",
    }
    out = rewrite_media_urls(html, url_map)
    assert "wp-content" not in out
    assert "/images/vue-1.png" in out
    assert "/images/vue-2.png" in out
```

- [ ] **Step 7: Run rewrite test — expect FAIL**

Run: `PYTHONPATH=. pytest tests/test_rewrite.py -v`
Expected: FAIL (missing module)

- [ ] **Step 8: Implement `rewrite.py`**

```python
from __future__ import annotations


def rewrite_media_urls(html: str, url_map: dict[str, str]) -> str:
    # Replace longer keys first to avoid partial overlaps
    out = html
    for old in sorted(url_map.keys(), key=len, reverse=True):
        out = out.replace(old, url_map[old])
    return out
```

- [ ] **Step 9: Run rewrite test — expect PASS**

Run: `PYTHONPATH=. pytest tests/test_rewrite.py -v`
Expected: PASS

- [ ] **Step 10: Commit**

```bash
git add scripts
git commit -m "$(cat <<'EOF'
feat: add WXR parser and media URL rewrite helpers

Introduce tested Python helpers that extract WordPress items and map
upload URLs to /images/ paths for the Hugo migration.
EOF
)"
```

---

### Task 3: Media downloader + Markdown writer + CLI

**Files:**
- Create: `scripts/wxr_migrate/media.py`
- Create: `scripts/wxr_migrate/write.py`
- Create: `scripts/wxr_migrate/__main__.py`
- Create: `scripts/tests/test_media.py`
- Create: `scripts/tests/test_write.py`
- Create: `scripts/tests/fixtures/mini-media.xml`

**Interfaces:**
- Consumes: `ContentItem`, media WXR path, output dirs
- Produces:
  - `build_media_map(media_wxr: Path, images_dir: Path, download: bool = True) -> dict[str, str]`  
    Maps each attachment’s absolute URL and path-only form → `/images/<safe_name>`. Downloads when `download=True`. On HTTP failure: log warning, skip entry, continue. Collision: if basename exists for a different source URL, use `<stem>-<sha1[:8]><suffix>`.
  - `html_to_markdown(html: str) -> str` using html2text
  - `write_content(items: list[ContentItem], url_map: dict[str, str], content_dir: Path) -> tuple[int, int]`  
    Filters `status=="publish"` and `post_type in {"post","page"}`. Raises `ValueError` on empty title or empty slug or duplicate slug across posts+pages. Posts → `content_dir/blog/<slug>.md`; pages → `content_dir/<slug>.md`. Returns `(posts_written, pages_written)`.
  - CLI: `python -m wxr_migrate --posts PATH --pages PATH --media PATH --site-content PATH --images-dir PATH [--dry-run-media]`

- [ ] **Step 1: Write failing media naming test**

`scripts/tests/test_media.py`:

```python
from pathlib import Path
from wxr_migrate.media import choose_filename


def test_choose_filename_avoids_collision(tmp_path: Path):
    (tmp_path / "vue-1.png").write_bytes(b"a")
    name = choose_filename(
        source_url="https://panjigautama.com/wp-content/uploads/2022/01/vue-1.png",
        images_dir=tmp_path,
        reserved={"vue-1.png": "https://other/vue-1.png"},
    )
    assert name != "vue-1.png"
    assert name.endswith(".png")
```

- [ ] **Step 2: Run — expect FAIL**

Run: `PYTHONPATH=. pytest tests/test_media.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `media.py`**

```python
from __future__ import annotations

from hashlib import sha1
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET
import warnings

NS = {"wp": "http://wordpress.org/export/1.2/"}


def choose_filename(source_url: str, images_dir: Path, reserved: dict[str, str]) -> str:
    path = unquote(urlparse(source_url).path)
    base = PurePosixPath(path).name or "file.bin"
    existing = reserved.get(base)
    if existing is None or existing == source_url:
        return base
    stem = PurePosixPath(base).stem
    suffix = PurePosixPath(base).suffix
    digest = sha1(source_url.encode()).hexdigest()[:8]
    return f"{stem}-{digest}{suffix}"


def build_media_map(media_wxr: Path, images_dir: Path, download: bool = True) -> dict[str, str]:
    images_dir.mkdir(parents=True, exist_ok=True)
    tree = ET.parse(media_wxr)
    channel = tree.getroot().find("channel")
    if channel is None:
        raise ValueError(f"No channel in {media_wxr}")

    reserved: dict[str, str] = {}
    url_map: dict[str, str] = {}
    missing: list[str] = []

    for item in channel.findall("item"):
        post_type = (item.findtext("wp:post_type", default="", namespaces=NS) or "").strip()
        if post_type != "attachment":
            continue
        attachment_url = (item.findtext("wp:attachment_url", default="", namespaces=NS) or "").strip()
        if not attachment_url:
            continue

        filename = choose_filename(attachment_url, images_dir, reserved)
        reserved[filename] = attachment_url
        dest = images_dir / filename
        public_path = f"/images/{filename}"

        parsed = urlparse(attachment_url)
        path_only = parsed.path
        url_map[attachment_url] = public_path
        url_map[path_only] = public_path

        if not download:
            continue
        if dest.exists() and dest.stat().st_size > 0:
            continue
        try:
            req = Request(attachment_url, headers={"User-Agent": "panjigautama-hugo-migrate/1.0"})
            with urlopen(req, timeout=60) as resp:
                dest.write_bytes(resp.read())
        except Exception as exc:  # noqa: BLE001 — continue on any download failure
            missing.append(attachment_url)
            warnings.warn(f"Failed to download {attachment_url}: {exc}")

    if missing:
        print("MISSING_MEDIA:")
        for url in missing:
            print(url)
    return url_map
```

- [ ] **Step 4: Run media test — expect PASS**

Run: `PYTHONPATH=. pytest tests/test_media.py -v`
Expected: PASS

- [ ] **Step 5: Write failing write test**

`scripts/tests/test_write.py`:

```python
from pathlib import Path
from wxr_migrate.parse import ContentItem
from wxr_migrate.write import write_content


def test_write_content_posts_and_pages(tmp_path: Path):
    items = [
        ContentItem(
            title="Hello",
            slug="hello",
            date="2021-01-15 10:00:00",
            lastmod="2021-01-16 11:00:00",
            status="publish",
            post_type="post",
            categories=["Management"],
            tags=[],
            content_html='<p>Hi <img src="https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png" /></p>',
        ),
        ContentItem(
            title="About Me",
            slug="about-me",
            date="2021-01-01 10:00:00",
            lastmod="2021-01-01 10:00:00",
            status="publish",
            post_type="page",
            categories=[],
            tags=[],
            content_html="<p>About</p>",
        ),
        ContentItem(
            title="Draft",
            slug="draft",
            date="2021-01-01 10:00:00",
            lastmod="2021-01-01 10:00:00",
            status="draft",
            post_type="post",
            categories=[],
            tags=[],
            content_html="<p>x</p>",
        ),
    ]
    url_map = {
        "https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png": "/images/vue-1.png",
        "/wp-content/uploads/2021/01/vue-1.png": "/images/vue-1.png",
    }
    posts, pages = write_content(items, url_map, tmp_path)
    assert posts == 1
    assert pages == 1
    post = (tmp_path / "blog" / "hello.md").read_text()
    assert 'title: "Hello"' in post
    assert "categories:" in post
    assert "/images/vue-1.png" in post
    assert "wp-content" not in post
    assert (tmp_path / "about-me.md").exists()
```

- [ ] **Step 6: Run write test — expect FAIL**

Run: `PYTHONPATH=. pytest tests/test_write.py -v`
Expected: FAIL

- [ ] **Step 7: Implement `write.py`**

```python
from __future__ import annotations

from pathlib import Path
import html2text

from wxr_migrate.parse import ContentItem
from wxr_migrate.rewrite import rewrite_media_urls


def html_to_markdown(html: str) -> str:
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.body_width = 0
    converter.protect_links = True
    return converter.handle(html).strip() + "\n"


def _yaml_list(name: str, values: list[str]) -> str:
    if not values:
        return ""
    lines = "\n".join(f'  - "{v.replace(chr(34), "")}"' for v in values)
    return f"{name}:\n{lines}\n"


def write_content(
    items: list[ContentItem],
    url_map: dict[str, str],
    content_dir: Path,
) -> tuple[int, int]:
    content_dir.mkdir(parents=True, exist_ok=True)
    blog_dir = content_dir / "blog"
    blog_dir.mkdir(parents=True, exist_ok=True)

    seen: set[str] = set()
    posts = pages = 0

    for item in items:
        if item.status != "publish" or item.post_type not in {"post", "page"}:
            continue
        if not item.title.strip():
            raise ValueError(f"Empty title for slug={item.slug!r}")
        if not item.slug.strip():
            raise ValueError(f"Empty slug for title={item.title!r}")
        if item.slug in seen:
            raise ValueError(f"Duplicate slug: {item.slug}")
        seen.add(item.slug)

        rewritten = rewrite_media_urls(item.content_html, url_map)
        body = html_to_markdown(rewritten)
        # Keep raw HTML if conversion emptied meaningful content but HTML had tags
        if not body.strip() and "<" in item.content_html:
            body = rewritten.strip() + "\n"

        fm = (
            "---\n"
            f'title: "{item.title.replace(chr(34), "")}"\n'
            f'date: {item.date.replace(" ", "T")}\n'
            f'lastmod: {item.lastmod.replace(" ", "T")}\n'
            f'slug: "{item.slug}"\n'
            f"draft: false\n"
            f"{_yaml_list('categories', item.categories)}"
            f"{_yaml_list('tags', item.tags)}"
            "---\n\n"
        )

        if item.post_type == "post":
            path = blog_dir / f"{item.slug}.md"
            posts += 1
        else:
            path = content_dir / f"{item.slug}.md"
            pages += 1
        path.write_text(fm + body, encoding="utf-8")

    return posts, pages
```

- [ ] **Step 8: Implement CLI `__main__.py`**

```python
from __future__ import annotations

import argparse
from pathlib import Path

from wxr_migrate.media import build_media_map
from wxr_migrate.parse import parse_wxr
from wxr_migrate.write import write_content


def main() -> None:
    p = argparse.ArgumentParser(description="Migrate WordPress WXR to Hugo Markdown")
    p.add_argument("--posts", type=Path, required=True)
    p.add_argument("--pages", type=Path, required=True)
    p.add_argument("--media", type=Path, required=True)
    p.add_argument("--site-content", type=Path, required=True)
    p.add_argument("--images-dir", type=Path, required=True)
    p.add_argument("--dry-run-media", action="store_true", help="Build URL map without downloading")
    args = p.parse_args()

    url_map = build_media_map(args.media, args.images_dir, download=not args.dry_run_media)
    items = parse_wxr(args.posts) + parse_wxr(args.pages)
    posts, pages = write_content(items, url_map, args.site_content)
    print(f"Wrote {posts} posts and {pages} pages; media map size={len(url_map)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 9: Run all script tests — expect PASS**

Run: `cd scripts && source .venv/bin/activate && PYTHONPATH=. pytest -v`
Expected: all PASS

- [ ] **Step 10: Commit**

```bash
git add scripts
git commit -m "$(cat <<'EOF'
feat: add media download and Markdown writer CLI

Complete the WXR migration pipeline so posts/pages become Hugo content
with /images/ media references.
EOF
)"
```

---

### Task 4: Run migration against real WordPress backups

**Files:**
- Generate: `site/content/blog/*.md` (≈45)
- Generate: `site/content/about-me.md`, `privacy-policy.md`, `engineering-lead-materials.md`
- Generate: `site/static/images/*`
- Keep: `site/content/_index.md`, `site/content/blog/_index.md` (do not overwrite)

**Interfaces:**
- Consumes: Task 3 CLI
- Produces: full content tree ready for Hugo

- [ ] **Step 1: Run converter**

```bash
cd /Users/panji.gautama/Documents/Project/panjigautamacom-blog
source scripts/.venv/bin/activate
PYTHONPATH=scripts python -m wxr_migrate \
  --posts wordpress-backup/panjigautama.WordPress.2026-07-31.posts.xml \
  --pages wordpress-backup/panjigautama.WordPress.2026-07-31.pages.xml \
  --media wordpress-backup/panjigautama.WordPress.2026-07-31.media.xml \
  --site-content site/content \
  --images-dir site/static/images
```

Expected: `Wrote 45 posts and 3 pages; ...` (exact counts may vary slightly if WXR differs; investigate if posts ≠ 45 or pages ≠ 3). Print `MISSING_MEDIA:` list if any downloads failed — retry those URLs once.

- [ ] **Step 2: Spot-check counts**

```bash
ls site/content/blog/*.md | wc -l
ls site/content/*.md
ls site/static/images | wc -l
rg -l 'wp-content/uploads' site/content || true
```

Expected: blog markdown count ≈ 45; three page files among content root; little or no remaining `wp-content/uploads` in content (favicon-only mentions OK if any).

- [ ] **Step 3: Hugo build**

Run: `cd site && hugo --minify`
Expected: exit 0

- [ ] **Step 4: Commit generated content and images**

```bash
git add site/content site/static/images
git commit -m "$(cat <<'EOF'
feat: import WordPress posts, pages, and media into Hugo

Convert published WXR content to Markdown with rewritten /images/
media paths for local Hugo builds.
EOF
)"
```

---

### Task 5: Favicon + Google Analytics

**Files:**
- Modify: `site/static/images/favicon.png` (download/copy from live site)
- Create optional: `site/static/favicon.ico`
- Modify: `site/layouts/partials/custom_head.html`
- Confirm: `site/hugo.toml` has `params.favicon = "images/favicon.png"`

**Interfaces:**
- Consumes: Bear Blog `favicon.html` + `custom_head.html` hooks
- Produces: favicon in browser tab; GA4 `G-60P3WJPWMJ` on every page

- [ ] **Step 1: Download favicon assets**

```bash
cd site/static/images
curl -fsSL -o favicon.png \
  "https://panjigautama.com/wp-content/uploads/2021/01/ico.png"
# optional ico for browsers that request /favicon.ico
mkdir -p ../
curl -fsSL -o ../favicon.ico \
  "https://panjigautama.com/wp-content/uploads/2021/01/cropped-ico-32x32.png" \
  || cp favicon.png ../favicon.ico
```

Expected: `site/static/images/favicon.png` non-empty

- [ ] **Step 2: Write GA + ensure favicon param**

Replace `site/layouts/partials/custom_head.html` with:

```html
<!-- Google Analytics GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-60P3WJPWMJ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-60P3WJPWMJ');
</script>
```

Confirm `site/hugo.toml` contains:

```toml
favicon = "images/favicon.png"
```

- [ ] **Step 3: Verify in built HTML**

```bash
cd site && hugo --minify
rg -n 'G-60P3WJPWMJ' public/index.html
rg -n 'favicon' public/index.html
```

Expected: both match

- [ ] **Step 4: Commit**

```bash
git add site/static/images/favicon.png site/static/favicon.ico site/layouts/partials/custom_head.html site/hugo.toml
git commit -m "$(cat <<'EOF'
feat: add site favicon and Google Analytics GA4

Wire Bear Blog custom_head with measurement ID G-60P3WJPWMJ and
serve the existing panjigautama.com icon from static assets.
EOF
)"
```

---

### Task 6: Homepage copy + menu pages alignment

**Files:**
- Modify: `site/content/_index.md` (short personal intro; link to `/blog/`)
- Verify pages exist at root: `about-me`, `privacy-policy`, `engineering-lead-materials`
- Optional: add Bear Blog-style menu via homepage markdown links (Bear Blog uses markdown links on `_index` / header — check theme `header.html`; if header is only title, put nav links in `_index.md`)

**Interfaces:**
- Consumes: migrated pages
- Produces: usable homepage matching Bear Blog minimal style

- [ ] **Step 1: Inspect theme header**

Run: `sed -n '1,80p' site/themes/hugo-bearblog/layouts/partials/header.html`
Expected: understand how nav works (often links defined in content)

- [ ] **Step 2: Update homepage**

Set `site/content/_index.md` to something like:

```markdown
---
title: "Home"
---

I'm Panji Gautama. I write about engineering leadership, product, and how I work.

- [Blog](/blog/)
- [About Me](/about-me/)
- [Engineering Lead Materials](/engineering-lead-materials/)
- [Privacy Policy](/privacy-policy/)
```

- [ ] **Step 3: Local server smoke (manual)**

Run: `cd site && hugo server -D`
Visit: `http://localhost:1313/`, `/blog/`, one post URL e.g. `/muhasabah/`, `/about-me/`, `/categories/management/` (or whatever category slug Hugo generates)

Expected: all 200; images load from `/images/...`

- [ ] **Step 4: Commit**

```bash
git add site/content/_index.md
git commit -m "$(cat <<'EOF'
content: tighten homepage with Bear Blog navigation links

Point visitors to blog and key pages after the WordPress import.
EOF
)"
```

---

### Task 7: Dockerfile, Compose, Caddy snippet

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`
- Create: `Caddyfile.snippet`
- Create: `.dockerignore`

**Interfaces:**
- Consumes: `site/` Hugo project
- Produces: container listening on `:8080` serving static files; documented host Caddy block

- [ ] **Step 1: Write `.dockerignore`**

```text
.git
scripts/.venv
site/public
**/__pycache__
*.md
!site/content/**/*.md
wordpress-backup
docs
```

- [ ] **Step 2: Write multi-stage `Dockerfile`**

```dockerfile
# syntax=docker/dockerfile:1
FROM hugomods/hugo:exts AS build
WORKDIR /src
COPY site/ /src/
RUN hugo --minify

FROM caddy:2-alpine
COPY --from=build /src/public /srv
COPY <<EOF /etc/caddy/Caddyfile
:8080 {
    root * /srv
    encode gzip
    file_server
    try_files {path} {path}/ /index.html
}
EOF
EXPOSE 8080
```

Note: if heredoc `COPY <<EOF` is unsupported in the Docker version on the VPS, replace with a small `docker/Caddyfile.container` file copied in.

Fallback file `docker/Caddyfile.container`:

```caddy
:8080 {
    root * /srv
    encode gzip
    file_server
}
```

And Dockerfile serve stage:

```dockerfile
FROM caddy:2-alpine
COPY --from=build /src/public /srv
COPY docker/Caddyfile.container /etc/caddy/Caddyfile
EXPOSE 8080
```

Prefer the fallback file approach for portability — **use the fallback in the implementation**.

- [ ] **Step 3: Write `docker-compose.yml`**

```yaml
services:
  blog:
    build: .
    container_name: panjigautama-hugo
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"
```

- [ ] **Step 4: Write `Caddyfile.snippet`**

```caddy
# Merge into the host Caddyfile (TLS already handled by host Caddy).
# Adjust upstream if Compose publishes a different port/host.
panjigautama.com, www.panjigautama.com {
    encode gzip
    reverse_proxy 127.0.0.1:8080
}
```

- [ ] **Step 5: Build and run locally**

```bash
docker compose build
docker compose up -d
curl -sI http://127.0.0.1:8080/ | head -5
curl -s http://127.0.0.1:8080/ | rg -n 'G-60P3WJPWMJ|Panji'
curl -sI http://127.0.0.1:8080/about-me/ | head -5
```

Expected: HTTP 200; GA ID and site title present; about page 200

- [ ] **Step 6: Commit**

```bash
git add Dockerfile docker-compose.yml Caddyfile.snippet .dockerignore docker/Caddyfile.container
git commit -m "$(cat <<'EOF'
feat: add Docker Compose static serving for Hugo blog

Build Hugo in-image and expose Caddy on localhost:8080 for the host
reverse proxy on the VPS.
EOF
)"
```

---

### Task 8: Local QA checklist (acceptance)

**Files:**
- None required (verification only); optionally Create: `docs/qa-checklist.md` with results dated

**Interfaces:**
- Consumes: running `hugo server` or Compose from Task 7
- Produces: documented pass/fail against design success criteria

- [ ] **Step 1: Run checklist against Compose (`http://127.0.0.1:8080`)**

Verify each:

1. Homepage loads
2. `/blog/` lists posts
3. At least 5 sample posts at root URLs (pick from WP: `/muhasabah/`, `/api-key-best-practices/`, `/silent-meeting/`, `/new-chapter-of-kudo/`, `/facilitating-a-great-meeting/`) return 200
4. `/about-me/`, `/privacy-policy/`, `/engineering-lead-materials/` return 200
5. A category page under `/categories/...` returns 200 and lists posts
6. An image from a post body returns 200 under `/images/...`
7. HTML contains `G-60P3WJPWMJ`
8. Favicon link present / `/images/favicon.png` returns 200
9. No requirement to serve `/wp-content/uploads/...` (404 is acceptable)

Commands:

```bash
for p in / /blog/ /muhasabah/ /about-me/ /images/favicon.png; do
  echo -n "$p "
  curl -s -o /dev/null -w "%{http_code}\n" "http://127.0.0.1:8080$p"
done
```

Expected: `200` for each listed path that exists

- [ ] **Step 2: Record results**

Write `docs/qa-checklist.md` with date and pass/fail table.

- [ ] **Step 3: Commit QA notes + push**

```bash
git add docs/qa-checklist.md
git commit -m "$(cat <<'EOF'
docs: record local Hugo migration QA checklist results

Capture acceptance checks before VPS cutover.
EOF
)"
git push origin main
```

---

### Task 9: VPS cutover runbook

**Files:**
- Create: `docs/operations-cutover.md`

**Interfaces:**
- Consumes: Compose + Caddyfile.snippet
- Produces: operator steps for deploy, verify, rollback (48–72h WP window)

- [ ] **Step 1: Write runbook**

`docs/operations-cutover.md` must include:

1. SSH to VPS; `git clone`/`git pull` `https://github.com/rhapsodixx/panjigautama-hugo.git`
2. Init submodules: `git submodule update --init --recursive`
3. `docker compose build && docker compose up -d`
4. Confirm `curl -sI http://127.0.0.1:8080/` → 200
5. Merge `Caddyfile.snippet` into host Caddyfile; `caddy reload` (or distro-equivalent)
6. Stop/disable WordPress + LiteSpeed vhost for panjigautama.com **without deleting** data for 48–72h
7. Production checks: HTTPS, sample posts, favicon, GA network request
8. Rollback: restore prior Caddy site block to WP upstream; `docker compose stop`

- [ ] **Step 2: Commit and push**

```bash
git add docs/operations-cutover.md
git commit -m "$(cat <<'EOF'
docs: add VPS cutover and rollback runbook

Document Compose deploy, host Caddy merge, and WordPress rollback window.
EOF
)"
git push origin main
```

- [ ] **Step 3: Stop — do not execute production cutover unless user explicitly asks**

Cutover on the live VPS is a **manual operator action** gated on user request after local QA passes.

---

## Self-review (plan vs spec)

| Spec requirement | Task |
|------------------|------|
| Hugo + hugo-bearblog | Task 1 |
| Root-level URLs | Task 1 permalinks + Task 4 content |
| WXR → Markdown script | Tasks 2–4 |
| Media → `/images/` + rewrite | Tasks 2–4 |
| No `/wp-content/` redirects | Tasks 3–4, 8 |
| Categories as taxonomies | Task 1 (enabled) + Task 4 front matter |
| Favicon from live site | Task 5 |
| GA `G-60P3WJPWMJ` | Task 5 |
| Docker Compose build-on-VPS | Task 7 |
| Host Caddy snippet | Task 7–9 |
| Local first then cutover | Tasks 8–9 |
| Drop comments | Tasks 2–4 (never exported) |
| Error handling (media miss, slug collision) | Task 3 |
| AGENTS/CLAUDE/ADRs/repo | Already done |

No intentional placeholders remain. Bear Blog exampleSite’s `disableKinds = ["taxonomy"]` is explicitly overridden in Global Constraints and Task 1.
