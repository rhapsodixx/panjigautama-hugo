from __future__ import annotations


def rewrite_media_urls(html: str, url_map: dict[str, str]) -> str:
    # Replace longer keys first to avoid partial overlaps
    out = html
    for old in sorted(url_map.keys(), key=len, reverse=True):
        out = out.replace(old, url_map[old])
    return out
