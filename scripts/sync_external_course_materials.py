#!/usr/bin/env python3
"""Synchronize public professor-hosted PDFs into a course material release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


USER_AGENT = "2026-fall-study-hub-material-sync/1.0"
COURSE_SLUG = re.compile(r"^[a-z0-9_]+$")
SAFE_FILENAME = re.compile(r"^[^/\\\x00-\x1f]+$")


@dataclass(frozen=True)
class MaterialLink:
    filename: str
    label: str
    source_url: str


class ScheduleTopicPdfParser(HTMLParser):
    """Collect anchors from the Topic column of the schedule table."""

    def __init__(self, section_id: str) -> None:
        super().__init__(convert_charrefs=True)
        self.section_id = section_id
        self.in_schedule = False
        self.in_table = False
        self.in_row = False
        self.cell_index = -1
        self.anchor_href: str | None = None
        self.anchor_text: list[str] = []
        self.links: list[tuple[str, str]] = []

    @staticmethod
    def _attributes(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key: value or "" for key, value in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = self._attributes(attrs)
        if tag == "section" and attributes.get("id") == self.section_id:
            self.in_schedule = True
            return
        if not self.in_schedule:
            return
        if tag == "table":
            self.in_table = True
        elif tag == "tr" and self.in_table:
            self.in_row = True
            self.cell_index = -1
        elif tag in {"td", "th"} and self.in_row:
            self.cell_index += 1
        elif tag == "a" and self.in_row and self.cell_index == 1:
            href = attributes.get("href", "").strip()
            if href:
                self.anchor_href = href
                self.anchor_text = []

    def handle_data(self, data: str) -> None:
        if self.anchor_href is not None:
            self.anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.anchor_href is not None:
            label = " ".join("".join(self.anchor_text).split())
            self.links.append((self.anchor_href, label))
            self.anchor_href = None
            self.anchor_text = []
        elif tag == "tr" and self.in_row:
            self.in_row = False
            self.cell_index = -1
        elif tag == "table" and self.in_table:
            self.in_table = False
        elif tag == "section" and self.in_schedule:
            self.in_schedule = False


def fetch_bytes(url: str, *, timeout: int = 30, attempts: int = 3) -> tuple[bytes, str]:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
            with urlopen(request, timeout=timeout) as response:
                status = getattr(response, "status", 200)
                if status != 200:
                    raise RuntimeError(f"HTTP {status} for {url}")
                return response.read(), response.headers.get("Content-Type", "")
        except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(1 + attempt)
    raise RuntimeError(f"Failed to download {url}: {last_error}") from last_error


def parse_material_links(html: str, source_page: str, section_id: str = "schedule") -> list[MaterialLink]:
    parser = ScheduleTopicPdfParser(section_id)
    parser.feed(html)

    source = urlsplit(source_page)
    source_prefix = source.path if source.path.endswith("/") else source.path.rsplit("/", 1)[0] + "/"
    found: dict[str, MaterialLink] = {}
    for href, label in parser.links:
        resolved = urlsplit(urljoin(source_page, href))
        if (resolved.scheme.casefold(), resolved.netloc.casefold()) != (
            source.scheme.casefold(),
            source.netloc.casefold(),
        ):
            continue
        if not resolved.path.startswith(source_prefix) or not resolved.path.casefold().endswith(".pdf"):
            continue
        filename = unquote(resolved.path.rsplit("/", 1)[-1])
        if not filename or not SAFE_FILENAME.fullmatch(filename) or filename in {".", ".."}:
            raise RuntimeError(f"Unsafe material filename in {href!r}")
        clean_url = urlunsplit((resolved.scheme, resolved.netloc, resolved.path, "", ""))
        material = MaterialLink(filename=filename, label=label or filename, source_url=clean_url)
        previous = found.get(filename.casefold())
        if previous and previous.source_url != material.source_url:
            raise RuntimeError(f"Conflicting URLs for {filename}")
        found[filename.casefold()] = material

    if not found:
        raise RuntimeError(f"No same-site PDF links found in #{section_id} Topic column")
    return sorted(found.values(), key=lambda item: natural_key(item.filename))


def natural_key(value: str) -> tuple[Any, ...]:
    return tuple(int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", value))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def cache_slug(filename: str) -> str:
    stem = Path(filename).stem.casefold()
    slug = re.sub(r"[^a-z0-9._-]+", ".", stem)
    slug = re.sub(r"\.{2,}", ".", slug).strip("._-")
    return slug or f"pdf-{hashlib.sha256(filename.encode('utf-8')).hexdigest()[:12]}"


def download_materials(links: list[MaterialLink], output: Path) -> list[dict[str, Any]]:
    output.mkdir(parents=True, exist_ok=True)
    materials: list[dict[str, Any]] = []
    for link in links:
        payload, content_type = fetch_bytes(link.source_url)
        if not payload.startswith(b"%PDF-"):
            raise RuntimeError(f"Downloaded file is not a PDF: {link.source_url} ({content_type})")
        target = (output / link.filename).resolve()
        target.relative_to(output.resolve())
        target.write_bytes(payload)
        materials.append(
            {
                "filename": link.filename,
                "label": link.label,
                "source_url": link.source_url,
                "sha256": sha256_bytes(payload),
                "size": len(payload),
                "path": str(target),
            }
        )
    return materials


def run_gh(gh: str, arguments: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([gh, *arguments], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"gh {' '.join(arguments)} failed: {detail}")
    return result


def release_payload(gh: str, repository: str, tag: str) -> dict[str, Any] | None:
    result = run_gh(
        gh,
        ["release", "view", tag, "--repo", repository, "--json", "assets,url,name,tagName"],
        check=False,
    )
    if result.returncode != 0:
        return None
    payload = json.loads(result.stdout or "{}")
    if not isinstance(payload, dict):
        raise RuntimeError("Unexpected GitHub release response")
    return payload


def ensure_release(gh: str, repository: str, tag: str, config: dict[str, Any]) -> dict[str, Any]:
    existing = release_payload(gh, repository, tag)
    if existing is not None:
        return existing
    run_gh(
        gh,
        [
            "release",
            "create",
            tag,
            "--repo",
            repository,
            "--target",
            str(config.get("target_branch") or "v5"),
            "--title",
            str(config["release_title"]),
            "--notes",
            "교수 제공 강의자료 공개 묶음입니다. 권리와 개인정보 범위를 확인한 뒤 사용하세요.",
        ],
    )
    created = release_payload(gh, repository, tag)
    if created is None:
        raise RuntimeError(f"Release was not created: {tag}")
    return created


def load_state(path: Path, config: dict[str, Any]) -> dict[str, Any]:
    if not path.is_file():
        return {"course": config["course"], "source_page": config["source_page"], "managed_assets": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("course") != config["course"] or payload.get("source_page") != config["source_page"]:
        raise RuntimeError(f"State does not match configuration: {path}")
    if not isinstance(payload.get("managed_assets"), list):
        raise RuntimeError(f"Invalid managed_assets state: {path}")
    return payload


def stable_state(config: dict[str, Any], materials: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "course": config["course"],
        "source_page": config["source_page"],
        "managed_assets": [
            {key: item[key] for key in ("filename", "label", "source_url", "sha256", "size")}
            for item in sorted(materials, key=lambda value: natural_key(str(value["filename"])))
        ],
    }


def write_json_if_changed(path: Path, payload: dict[str, Any]) -> bool:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    old = path.read_text(encoding="utf-8") if path.is_file() else None
    if old == rendered:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    return True


def render_materials_page(
    config: dict[str, Any],
    release_assets: list[dict[str, Any]],
    managed_materials: list[dict[str, Any]],
    site_base: str,
    repository: str,
) -> str:
    course = str(config["course"])
    title = str(config["course_title"])
    release_tag = str(config["release_tag"])
    release_url = f"https://github.com/{repository}/releases/tag/{release_tag}"
    upstream = {str(item["filename"]): item for item in managed_materials}
    lines = [
        "---",
        f"title: {json.dumps(title + ' 강의자료', ensure_ascii=False)}",
        "tags:",
        "  - course-materials",
        f"  - {course}",
        "review_status: approved",
        "---",
        "",
        f"# {title} 강의자료",
        "",
        f"전체 다운로드: [GitHub Release 열기]({release_url})",
        "",
        f"자동 동기화 원본: [SNU CSL 운영체제 강의 페이지]({config['source_page']})",
        "",
        "> [!warning]",
        "> 아래 파일은 교수 제공 자료이며 공개 범위와 이용 책임을 확인한 뒤 업로드되었습니다.",
        "",
        "## 파일",
        "",
    ]
    for asset in sorted(release_assets, key=lambda item: natural_key(str(item.get("name") or ""))):
        name = str(asset.get("name") or "")
        if not name:
            continue
        size = int(asset.get("size") or 0)
        asset_url = f"{site_base.rstrip('/')}/materials/{quote(course)}/{quote(name)}"
        line = f"- [`{name}`]({asset_url}) · {size / 1024 / 1024:.1f} MiB"
        source = upstream.get(name)
        if source:
            line += f" · [교수 사이트 원본]({source['source_url']})"
        if Path(name).suffix.casefold() == ".pdf":
            manifest = f"{site_base.rstrip('/')}/page_cache/{quote(course)}/{quote(cache_slug(name))}/manifest.json"
            line += f" · [페이지 캐시 manifest]({manifest})"
        lines.append(line)
    return "\n".join(lines) + "\n"


def write_text_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.is_file() else None
    if old == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def validate_config(payload: dict[str, Any]) -> dict[str, Any]:
    required = ("course", "course_title", "source_page", "release_tag", "release_title")
    missing = [key for key in required if not str(payload.get(key) or "").strip()]
    if missing:
        raise RuntimeError(f"Missing configuration field(s): {', '.join(missing)}")
    if not COURSE_SLUG.fullmatch(str(payload["course"])):
        raise RuntimeError(f"Invalid course slug: {payload['course']}")
    source = urlsplit(str(payload["source_page"]))
    if source.scheme != "https" or not source.netloc:
        raise RuntimeError("source_page must be an HTTPS URL")
    return payload


def synchronize(args: argparse.Namespace) -> dict[str, Any]:
    config = validate_config(json.loads(args.config.read_text(encoding="utf-8")))
    page_bytes, _ = fetch_bytes(str(config["source_page"]))
    html = page_bytes.decode("utf-8", errors="replace")
    links = parse_material_links(html, str(config["source_page"]), str(config.get("schedule_section_id") or "schedule"))
    minimum = int(config.get("minimum_materials") or 1)
    if len(links) < minimum:
        raise RuntimeError(f"Refusing sync: found {len(links)} material(s), expected at least {minimum}")
    materials = download_materials(links, args.download_dir)

    preview = {
        "changed": False,
        "release_changed": False,
        "state_changed": False,
        "materials_changed": False,
        "discovered": [item["filename"] for item in materials],
        "uploaded": [],
        "removed": [],
    }
    if not args.execute:
        return preview

    gh = args.gh or shutil.which("gh")
    if not gh:
        raise RuntimeError("GitHub CLI (gh) was not found")
    state = load_state(args.state, config)
    previous = {str(item["filename"]): item for item in state["managed_assets"]}
    current = {str(item["filename"]): item for item in materials}
    release = ensure_release(gh, args.repository, str(config["release_tag"]), config)
    assets = {str(item.get("name") or ""): item for item in release.get("assets", []) if item.get("name")}

    for name in sorted(previous.keys() - current.keys(), key=natural_key):
        if name in assets:
            run_gh(
                gh,
                ["release", "delete-asset", str(config["release_tag"]), name, "--yes", "--repo", args.repository],
            )
            preview["removed"].append(name)

    for name, item in sorted(current.items(), key=lambda pair: natural_key(pair[0])):
        existing = assets.get(name)
        digest = str(existing.get("digest") or "").removeprefix("sha256:") if existing else ""
        if existing and digest == item["sha256"]:
            continue
        if existing and name not in previous:
            raise RuntimeError(f"Refusing to overwrite untracked release asset: {name}")
        run_gh(
            gh,
            [
                "release",
                "upload",
                str(config["release_tag"]),
                str(item["path"]),
                "--clobber",
                "--repo",
                args.repository,
            ],
        )
        preview["uploaded"].append(name)

    preview["release_changed"] = bool(preview["uploaded"] or preview["removed"])
    refreshed_release = release_payload(gh, args.repository, str(config["release_tag"]))
    if refreshed_release is None:
        raise RuntimeError("Release disappeared during synchronization")
    release_assets = list(refreshed_release.get("assets") or [])
    state_payload = stable_state(config, materials)
    preview["state_changed"] = write_json_if_changed(args.state, state_payload)
    materials_text = render_materials_page(
        config,
        release_assets,
        materials,
        args.site_base,
        args.repository,
    )
    preview["materials_changed"] = write_text_if_changed(args.materials_file, materials_text)
    preview["changed"] = bool(
        preview["release_changed"] or preview["state_changed"] or preview["materials_changed"]
    )
    return preview


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--materials-file", type=Path, required=True)
    parser.add_argument("--download-dir", type=Path, default=Path("tmp/external-course-materials"))
    parser.add_argument("--site-base", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--gh", help="Path to GitHub CLI")
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    try:
        result = synchronize(args)
    except Exception as exc:  # noqa: BLE001 - CLI must fail with a concise actionable message.
        print(f"External material sync failed: {exc}", file=sys.stderr)
        return 1
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
