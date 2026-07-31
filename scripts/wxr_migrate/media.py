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
