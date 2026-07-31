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
