#!/usr/bin/env python3
"""Check emitted local page, image, stylesheet, and script targets before deploy."""
from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script", "source"} else None
        if key and values.get(key):
            self.references.append(values[key])


def local_target(source: str, href: str, site_base: str) -> str | None:
    base = site_base.rstrip("/")
    origin = urlsplit(base)
    source_slug = source[:-10] if source.endswith("index.html") else source[:-5]
    resolved = urlsplit(urljoin(base + "/" + source_slug, href))
    if resolved.scheme not in {"http", "https"} or resolved.netloc != origin.netloc:
        return None
    prefix = origin.path.rstrip("/")
    if resolved.path == prefix:
        return ""
    if not resolved.path.startswith(prefix + "/"):
        # A same-origin URL escaping the configured project still cannot refer
        # to this build. Report it explicitly instead of ignoring a lost prefix.
        return "../" + unquote(resolved.path.lstrip("/"))
    return unquote(resolved.path[len(prefix) + 1:])


def target_exists(public: Path, target: str) -> bool:
    path = public / target
    try:
        path.resolve().relative_to(public.resolve())
    except ValueError:
        return False
    return path.is_file() or (path / "index.html").is_file() or Path(str(path) + ".html").is_file()


def validate_links(public: Path, site_base: str, policy: dict | None = None, skip_release_assets: bool = False) -> tuple[list[str], int, int]:
    exceptions = {(item["source"], item["target"]) for item in (policy or {}).get("legacy_link_exceptions", []) if item.get("reason")}
    errors: set[str] = set()
    checked = 0
    retained = 0
    html_files = sorted(public.rglob("*.html"))
    if not html_files:
        return ["No generated HTML files found"], 0, 0
    for path in html_files:
        source = path.relative_to(public).as_posix()
        parser = References()
        parser.feed(path.read_text(encoding="utf-8"))
        for href in parser.references:
            target = local_target(source, href, site_base)
            if target is None or (skip_release_assets and target.startswith("materials/")):
                continue
            checked += 1
            if target_exists(public, target):
                continue
            if (source, target) in exceptions:
                retained += 1
                continue
            errors.add(f"{source}: missing target {target}")
    return sorted(errors), checked, retained


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--site-base", required=True)
    parser.add_argument("--policy", type=Path, default=ROOT / "scripts/public_validation_policy.json")
    parser.add_argument("--skip-release-assets", action="store_true", help="For local builds without downloaded Release assets only")
    args = parser.parse_args()
    policy = json.loads(args.policy.read_text(encoding="utf-8"))
    errors, checked, retained = validate_links(args.public, args.site_base, policy, args.skip_release_assets)
    for error in errors:
        print(error)
    print(f"Checked {checked} internal references; {len(errors)} error(s); {retained} documented archived-course exception(s).")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
