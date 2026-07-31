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
        if item.slug == "sprout-test":
            continue
        if item.post_type not in {"post", "page"}:
            continue
        is_privacy_draft = (
            item.post_type == "page"
            and item.slug == "privacy-policy"
            and item.status != "publish"
        )
        if item.status != "publish" and not is_privacy_draft:
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
