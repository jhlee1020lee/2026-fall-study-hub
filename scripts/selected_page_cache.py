"""Validate bounded, hash-pinned source-figure previews without releasing a PDF."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Callable
from urllib.parse import urlsplit

from note_validation import parse_frontmatter


SCHEMA = "selected_page_cache_v1"
MODE = "selected_pages"
SHA256 = re.compile(r"[0-9a-f]{64}")
COMPONENT = re.compile(r"[a-z0-9_][a-z0-9._-]*")


def is_selected_manifest(manifest: dict) -> bool:
    return (manifest.get("publication_mode") == MODE or manifest.get("schema") == SCHEMA
            or "selected_pages" in manifest)


def read_safe_file(path: Path, boundary: Path) -> bytes:
    """Reject escapes and symlink/junction components before reading a cache file."""
    path, boundary = path.absolute(), boundary.absolute()
    path.relative_to(boundary)
    path.resolve().relative_to(boundary.resolve())
    current = path
    while True:
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise ValueError("symlink or junction in selected cache")
        if current == boundary:
            break
        current = current.parent
    if not path.is_file():
        raise ValueError("missing selected-cache file")
    return path.read_bytes()


def validate_selected_manifest(
    manifest: dict,
    course: str,
    slug: str,
    read_bytes: Callable[[str], bytes],
    existing_files: set[str],
) -> None:
    """Require the exact selected pages, filenames, bytes and source metadata.

    ``existing_files`` and ``read_bytes`` must describe the same snapshot. Git
    index/revision callers supply blob bytes, never unstaged filesystem bytes.
    The private source PDF hash records provenance; no unavailable original is
    claimed to have been revalidated by this public-only check.
    """
    if manifest.get("schema") != SCHEMA or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        raise ValueError("unsupported selected-cache schema")
    if manifest.get("publication_mode") != MODE or manifest.get("source_pdf_public") is not False:
        raise ValueError("selected cache requires explicit private-source publication mode")
    if not COMPONENT.fullmatch(course) or not COMPONENT.fullmatch(slug) or manifest.get("course") != course:
        raise ValueError("invalid or mismatched selected-cache course/slug")
    for key in ("source_pdf", "source_url", "generated_at"):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            raise ValueError(f"missing selected-cache {key}")
    if "/" in manifest["source_pdf"] or "\\" in manifest["source_pdf"] or not manifest["source_pdf"].lower().endswith(".pdf"):
        raise ValueError("source_pdf must be a PDF filename, not a path")
    url = urlsplit(manifest["source_url"])
    if url.scheme != "https" or not url.netloc or url.username or url.password or manifest.get("source_url_kind") != "lecture_source_description":
        raise ValueError("selected-cache source URL must identify its HTTPS source-description page")
    if not SHA256.fullmatch(str(manifest.get("source_sha256", ""))):
        raise ValueError("missing selected-cache source SHA-256")
    total, selected, pages = manifest.get("total_pages"), manifest.get("selected_pages"), manifest.get("pages")
    if type(total) is not int or total < 2 or not isinstance(selected, list) or not selected:
        raise ValueError("invalid selected-cache page count")
    if any(type(number) is not int or number < 1 or number > total for number in selected):
        raise ValueError("selected-cache page out of range or not an integer")
    if selected != sorted(set(selected)) or len(selected) >= total:
        raise ValueError("selected pages must be a sorted, unique, proper subset")
    if not isinstance(pages, list) or len(pages) != len(selected):
        raise ValueError("selected-cache page entries must match selected_pages")
    content_prefix = f"content/page_cache/{course}/{slug}/"
    static_prefix = f"static/page_cache/{course}/{slug}/"
    expected_files = {content_prefix + "manifest.json"}
    width = max(3, len(str(total)))
    for number, page in zip(selected, pages):
        if not isinstance(page, dict) or type(page.get("pdf_page")) is not int or page["pdf_page"] != number:
            raise ValueError("selected-cache page sequence mismatch")
        stem = f"page-{number:0{width}d}"
        for kind, prefix, suffix in (("markdown", content_prefix, ".md"), ("png", static_prefix, ".png")):
            target = prefix + stem + suffix
            expected_files.add(target)
            if page.get(kind) != target or target not in existing_files:
                raise ValueError(f"missing or unsafe selected-cache {kind} for page {number}")
            expected_hash = page.get(kind + "_sha256")
            if not SHA256.fullmatch(str(expected_hash or "")):
                raise ValueError(f"missing selected-cache {kind} SHA-256")
            actual = read_bytes(target)
            if hashlib.sha256(actual).hexdigest() != expected_hash:
                raise ValueError(f"selected-cache {kind} hash drift on page {number}")
            if kind == "markdown":
                metadata, _ = parse_frontmatter(actual.decode("utf-8"))
                for key in ("course", "source_pdf", "source_url", "source_url_kind", "generated_at"):
                    if metadata.get(key) != manifest[key]:
                        raise ValueError(f"selected-cache wrapper {key} mismatch")
                if type(metadata.get("pdf_page")) is not int or metadata["pdf_page"] != number:
                    raise ValueError("selected-cache wrapper page mismatch")
                if metadata.get("source_pdf_public") is not False or metadata.get("publication_approved") is not True or metadata.get("review_status") != "approved" or metadata.get("draft") is not False:
                    raise ValueError("selected-cache wrapper publication metadata mismatch")
    actual_files = {name for name in existing_files if name.startswith((content_prefix, static_prefix))}
    if actual_files != expected_files:
        raise ValueError("unexpected or missing files in bounded selected cache")


def selected_cache_dirs(content_root: Path, static_root: Path) -> tuple[set[Path], set[Path]]:
    """Fail closed before stale cleanup; retain only valid selected-page caches."""
    content_dirs: set[Path] = set()
    static_dirs: set[Path] = set()
    for manifest_path in sorted(content_root.glob("*/*/manifest.json")):
        raw = read_safe_file(manifest_path, content_root).decode("utf-8")
        try:
            manifest = json.loads(raw)
        except ValueError as exc:
            if re.search(r'"(?:publication_mode|schema|selected_pages)"\s*:\s*(?:"(?:selected_pages|selected_page_cache_v1)"|\[)', raw):
                raise RuntimeError(f"Cannot safely inspect selected-cache manifest: {manifest_path}") from exc
            continue
        if not isinstance(manifest, dict) or not is_selected_manifest(manifest):
            continue
        course, slug = manifest_path.parent.parent.name, manifest_path.parent.name
        roots = {"content": content_root, "static": static_root}
        existing: set[str] = set()
        for prefix, root in roots.items():
            directory = root / course / slug
            if directory.exists():
                existing.update(f"{prefix}/page_cache/{course}/{slug}/{path.relative_to(directory).as_posix()}"
                                for path in directory.rglob("*"))

        def read(relative: str) -> bytes:
            prefix, cache, relative_course, relative_slug, name = relative.split("/")
            if cache != "page_cache" or relative_course != course or relative_slug != slug:
                raise ValueError("selected-cache path escapes its exact directory")
            return read_safe_file(roots[prefix] / course / slug / name, roots[prefix])

        try:
            validate_selected_manifest(manifest, course, slug, read, existing)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise RuntimeError(f"Invalid selected-page cache {manifest_path}: {exc}") from exc
        content_dirs.add(manifest_path.parent.resolve())
        static_dirs.add((static_root / course / slug).resolve())
    return content_dirs, static_dirs
