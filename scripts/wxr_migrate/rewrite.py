from __future__ import annotations

import re

# WordPress intermediate sizes: filename-WIDTHxHEIGHT.ext
_SIZE_VARIANT_RE = re.compile(
    r"(https?://panjigautama\.com)?/wp-content/uploads/"
    r"(?P<path>[^\s\"'<>]+?)"
    r"-(?P<w>\d+)x(?P<h>\d+)"
    r"(?P<ext>\.[A-Za-z0-9]+)"
)


def _lookup_candidates(url: str) -> list[str]:
    """Exact URL plus absolute/relative counterpart and WordPress -scaled form."""
    candidates = [url]
    if url.startswith("http"):
        rel = url.split("panjigautama.com", 1)[-1]
        if rel.startswith("/wp-content/"):
            candidates.append(rel)
    elif url.startswith("/wp-content/"):
        candidates.append(f"https://panjigautama.com{url}")

    # Large WP uploads store attachment_url as basename-scaled.ext
    scaled: list[str] = []
    for key in list(candidates):
        if "-scaled." in key:
            continue
        stem, _, ext = key.rpartition(".")
        if stem and ext:
            scaled.append(f"{stem}-scaled.{ext}")
    candidates.extend(scaled)
    return candidates


def rewrite_media_urls(html: str, url_map: dict[str, str]) -> str:
    # Replace longer keys first to avoid partial overlaps
    out = html
    for old in sorted(url_map.keys(), key=len, reverse=True):
        out = out.replace(old, url_map[old])

    def _replace_size_variant(match: re.Match[str]) -> str:
        full = match.group(0)
        prefix = match.group(1) or ""
        stripped = f"{prefix}/wp-content/uploads/{match.group('path')}{match.group('ext')}"
        for key in _lookup_candidates(stripped):
            if key in url_map:
                return url_map[key]
        return full

    return _SIZE_VARIANT_RE.sub(_replace_size_variant, out)
