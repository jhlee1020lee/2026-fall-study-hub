#!/usr/bin/env python3
"""Copy committed page-cache manifests and PNGs into the Quartz build output."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--content-cache", type=Path, default=Path("content/page_cache"))
    parser.add_argument("--static-cache", type=Path, default=Path("static/page_cache"))
    args = parser.parse_args()

    copied_manifests = 0
    if args.content_cache.exists():
        for manifest in args.content_cache.rglob("manifest.json"):
            relative = manifest.relative_to(args.content_cache)
            target = args.public / "page_cache" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(manifest, target)
            copied_manifests += 1

    copied_pngs = 0
    if args.static_cache.exists():
        target_root = args.public / "static" / "page_cache"
        if target_root.exists():
            shutil.rmtree(target_root)
        shutil.copytree(args.static_cache, target_root)
        copied_pngs = sum(1 for path in target_root.rglob("*.png") if path.is_file())

    print(f"Staged {copied_manifests} manifest(s) and {copied_pngs} PNG(s) for Pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
