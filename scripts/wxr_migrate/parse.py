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
