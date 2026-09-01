#!/usr/bin/env python3
"""Generate exact per-page Markdown and PNG caches for released course PDFs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


PDF_LABEL = re.compile(r"`(?P<name>[^`\r\n]+\.pdf)`", re.IGNORECASE)
CACHE_LINK = re.compile(r"\s+·\s+\[페이지 캐시 manifest\]\([^)]+\)\s*$")


@dataclass(frozen=True)
class PdfSource:
    course: str
    label: str
    asset_name: str
    pdf_path: Path
    cache_slug: str
    source_url: str
    manifest_url: str


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def filename_identity(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return "".join(character for character in normalized if character.isalnum())


def pdf_cache_slug(filename: str) -> str:
    stem = Path(filename).stem.casefold()
    slug = re.sub(r"[^a-z0-9._-]+", ".", stem)
    slug = re.sub(r"\.{2,}", ".", slug).strip("._-")
    if slug:
        return slug
    return f"pdf-{hashlib.sha256(filename.encode('utf-8')).hexdigest()[:12]}"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def require_tool(name: str) -> str:
    resolved = shutil.which(name)
    if not resolved:
        raise RuntimeError(f"Required PDF tool was not found: {name}")
    return resolved


def remove_tree(path: Path) -> None:
    if not path.exists():
        return
    last_error: OSError | None = None
    for _ in range(5):
        try:
            shutil.rmtree(path)
        except OSError as exc:
            last_error = exc
            if not path.exists():
                return
            time.sleep(0.2)
        else:
            return
    if last_error:
        raise last_error


def pdf_page_count(pdfinfo: str, pdf_path: Path) -> int:
    result = subprocess.run(
        [pdfinfo, str(pdf_path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", result.stdout)
    if not match:
        raise RuntimeError(f"Could not determine page count: {pdf_path}")
    return int(match.group(1))


def extract_page_text(pdftotext: str, pdf_path: Path, page_number: int) -> str:
    result = subprocess.run(
        [
            pdftotext,
            "-f",
            str(page_number),
            "-l",
            str(page_number),
            "-layout",
            "-enc",
            "UTF-8",
            "-nopgbrk",
            str(pdf_path),
            "-",
        ],
        check=True,
        capture_output=True,
    )
    text = result.stdout.decode("utf-8", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n\f")


def render_page_png(
    pdftoppm: str,
    pdf_path: Path,
    page_number: int,
    output_path: Path,
    dpi: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = output_path.with_suffix("")
    subprocess.run(
        [
            pdftoppm,
            "-f",
            str(page_number),
            "-l",
            str(page_number),
            "-r",
            str(dpi),
            "-png",
            "-singlefile",
            str(pdf_path),
            str(prefix),
        ],
        check=True,
        capture_output=True,
    )
    if not output_path.is_file():
        raise RuntimeError(f"PNG renderer produced no output: {output_path}")


def discover_sources(
    pdf_root: Path,
    materials_root: Path,
    site_base: str,
) -> tuple[list[PdfSource], dict[Path, str]]:
    sources: list[PdfSource] = []
    updated_materials: dict[Path, str] = {}
    seen_cache_keys: set[tuple[str, str]] = set()

    for materials_path in sorted(materials_root.glob("*/materials.md")):
        course = materials_path.parent.name
        course_pdf_root = pdf_root / course
        assets = sorted(path for path in course_pdf_root.glob("*") if path.is_file() and path.suffix.lower() == ".pdf")
        assets_by_identity: dict[str, list[Path]] = {}
        for asset in assets:
            assets_by_identity.setdefault(filename_identity(asset.name), []).append(asset)

        original_lines = materials_path.read_text(encoding="utf-8").splitlines()
        output_lines: list[str] = []
        for line in original_lines:
            label_match = PDF_LABEL.search(line)
            if not label_match or not line.lstrip().startswith("-"):
                output_lines.append(line)
                continue

            label = label_match.group("name")
            matches = assets_by_identity.get(filename_identity(label), [])
            if len(matches) != 1:
                raise RuntimeError(
                    f"Expected exactly one released PDF for {course}/{label}, found {len(matches)}"
                )
            pdf_path = matches[0]
            slug = pdf_cache_slug(pdf_path.name)
            cache_key = (course, slug)
            if cache_key in seen_cache_keys:
                raise RuntimeError(f"Duplicate page-cache slug: {course}/{slug}")
            seen_cache_keys.add(cache_key)

            encoded_course = quote(course)
            encoded_asset = quote(pdf_path.name)
            encoded_slug = quote(slug)
            source_url = f"{site_base}/materials/{encoded_course}/{encoded_asset}"
            manifest_url = f"{site_base}/page_cache/{encoded_course}/{encoded_slug}/manifest.json"
            sources.append(
                PdfSource(
                    course=course,
                    label=label,
                    asset_name=pdf_path.name,
                    pdf_path=pdf_path,
                    cache_slug=slug,
                    source_url=source_url,
                    manifest_url=manifest_url,
                )
            )

            base_line = CACHE_LINK.sub("", line)
            output_lines.append(f"{base_line} · [페이지 캐시 manifest]({manifest_url})")

        updated = "\n".join(output_lines) + "\n"
        if updated != materials_path.read_text(encoding="utf-8"):
            updated_materials[materials_path] = updated

    return sources, updated_materials


def cache_is_current(
    manifest_path: Path,
    static_dir: Path,
    source_sha256: str,
) -> bool:
    if not manifest_path.is_file():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if manifest.get("source_sha256") != source_sha256:
        return False
    pages = manifest.get("pages")
    if not isinstance(pages, list) or len(pages) != manifest.get("total_pages"):
        return False
    content_dir = manifest_path.parent
    for page in pages:
        if not isinstance(page, dict):
            return False
        markdown_name = Path(str(page.get("markdown") or "")).name
        png_name = Path(str(page.get("png") or "")).name
        if not markdown_name or not png_name:
            return False
        if not (content_dir / markdown_name).is_file() or not (static_dir / png_name).is_file():
            return False
    return True


def write_page_markdown(
    path: Path,
    source: PdfSource,
    page_number: int,
    generated_at: str,
    text: str,
) -> None:
    frontmatter = [
        "---",
        f"course: {yaml_string(source.course)}",
        f"source_pdf: {yaml_string(source.asset_name)}",
        f"pdf_page: {page_number}",
        f"source_url: {yaml_string(source.source_url)}",
        f"generated_at: {yaml_string(generated_at)}",
        "---",
        "",
    ]
    path.write_text("\n".join(frontmatter) + text + ("\n" if text else ""), encoding="utf-8")


def generate_pdf_cache(
    source: PdfSource,
    content_root: Path,
    static_root: Path,
    work_root: Path,
    site_base: str,
    dpi: int,
    pdftotext: str,
    pdftoppm: str,
    pdfinfo: str,
) -> int:
    source_hash = sha256_file(source.pdf_path)
    final_content_dir = content_root / source.course / source.cache_slug
    final_static_dir = static_root / source.course / source.cache_slug
    manifest_path = final_content_dir / "manifest.json"
    if cache_is_current(manifest_path, final_static_dir, source_hash):
        return 0

    total_pages = pdf_page_count(pdfinfo, source.pdf_path)
    generated_at = utc_timestamp()
    work_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="page-cache-", dir=work_root) as temp_name:
        temp_root = Path(temp_name)
        temp_content = temp_root / "content"
        temp_static = temp_root / "static"
        temp_content.mkdir(parents=True)
        temp_static.mkdir(parents=True)
        page_width = max(3, len(str(total_pages)))
        pages: list[dict[str, object]] = []

        for page_number in range(1, total_pages + 1):
            page_stem = f"page-{page_number:0{page_width}d}"
            markdown_name = f"{page_stem}.md"
            png_name = f"{page_stem}.png"
            page_text = extract_page_text(pdftotext, source.pdf_path, page_number)
            write_page_markdown(
                temp_content / markdown_name,
                source,
                page_number,
                generated_at,
                page_text,
            )
            render_page_png(pdftoppm, source.pdf_path, page_number, temp_static / png_name, dpi)
            markdown_path = f"content/page_cache/{source.course}/{source.cache_slug}/{markdown_name}"
            png_path = f"static/page_cache/{source.course}/{source.cache_slug}/{png_name}"
            pages.append(
                {
                    "pdf_page": page_number,
                    "markdown": markdown_path,
                    "markdown_url": (
                        f"{site_base}/page_cache/{quote(source.course)}/{quote(source.cache_slug)}/{page_stem}"
                    ),
                    "png": png_path,
                    "png_url": (
                        f"{site_base}/static/page_cache/{quote(source.course)}/{quote(source.cache_slug)}/{png_name}"
                    ),
                }
            )

        manifest = {
            "course": source.course,
            "source_pdf": source.asset_name,
            "source_url": source.source_url,
            "source_sha256": source_hash,
            "generated_at": generated_at,
            "total_pages": total_pages,
            "pages": pages,
        }
        (temp_content / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        if final_content_dir.exists():
            remove_tree(final_content_dir)
        if final_static_dir.exists():
            remove_tree(final_static_dir)
        final_content_dir.parent.mkdir(parents=True, exist_ok=True)
        final_static_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(temp_content, final_content_dir)
        shutil.copytree(temp_static, final_static_dir)

    return total_pages


def remove_stale_cache_dirs(root: Path, expected: set[Path]) -> int:
    removed = 0
    if not root.exists():
        return removed
    resolved_root = root.resolve()
    for course_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        for cache_dir in sorted(path for path in course_dir.iterdir() if path.is_dir()):
            resolved_cache = cache_dir.resolve()
            resolved_cache.relative_to(resolved_root)
            if resolved_cache in expected:
                continue
            remove_tree(resolved_cache)
            removed += 1
        if not any(course_dir.iterdir()):
            course_dir.rmdir()
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-root", type=Path, required=True)
    parser.add_argument("--materials-root", type=Path, default=Path("content/courses"))
    parser.add_argument("--content-root", type=Path, default=Path("content/page_cache"))
    parser.add_argument("--static-root", type=Path, default=Path("static/page_cache"))
    parser.add_argument("--work-root", type=Path, default=Path("tmp/pdfs"))
    parser.add_argument("--site-base", required=True)
    parser.add_argument("--dpi", type=int, default=144)
    args = parser.parse_args()

    if args.dpi < 72 or args.dpi > 300:
        raise SystemExit("--dpi must be between 72 and 300")
    site_base = args.site_base.rstrip("/")
    pdftotext = require_tool("pdftotext")
    pdftoppm = require_tool("pdftoppm")
    pdfinfo = require_tool("pdfinfo")

    args.content_root.mkdir(parents=True, exist_ok=True)
    args.static_root.mkdir(parents=True, exist_ok=True)
    sources, updated_materials = discover_sources(args.pdf_root, args.materials_root, site_base)
    expected_content = {(args.content_root / source.course / source.cache_slug).resolve() for source in sources}
    expected_static = {(args.static_root / source.course / source.cache_slug).resolve() for source in sources}
    removed = remove_stale_cache_dirs(args.content_root, expected_content)
    removed += remove_stale_cache_dirs(args.static_root, expected_static)

    generated_pdfs = 0
    generated_pages = 0
    unchanged_pdfs = 0
    for source in sources:
        print(f"Checking {source.course}/{source.asset_name}", flush=True)
        pages = generate_pdf_cache(
            source,
            args.content_root,
            args.static_root,
            args.work_root,
            site_base,
            args.dpi,
            pdftotext,
            pdftoppm,
            pdfinfo,
        )
        if pages:
            generated_pdfs += 1
            generated_pages += pages
        else:
            unchanged_pdfs += 1

    for path, content in updated_materials.items():
        path.write_text(content, encoding="utf-8")

    print(
        "Page cache refresh complete: "
        f"sources={len(sources)}, generated_pdfs={generated_pdfs}, "
        f"generated_pages={generated_pages}, unchanged_pdfs={unchanged_pdfs}, "
        f"removed_stale_dirs={removed}, updated_material_pages={len(updated_materials)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
