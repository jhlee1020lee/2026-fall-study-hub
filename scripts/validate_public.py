#!/usr/bin/env python3
"""Fail closed when private course data is about to enter the public site."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from note_validation import parse_frontmatter, validate_lecture_note


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PARTS = {
    ".ssh",
    "_drafts",
    "_study_workbench",
    "03_recording_stt",
    "05_participants",
    "participants",
    "recordings",
    "private",
}
TEXT_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".ts", ".tsx", ".py", ".js", ".mjs", ".txt", ".csv", ".html", ".xml", ".toml", ".ini", ".cfg", ".sh", ".ps1", ".pem", ".key"}
SENSITIVE_FILENAMES = {"credentials.json", "cookies.json", "cookies.txt", "storage_state.json", "id_rsa", "id_ed25519"}
ENV_TEMPLATES = {".env.example", ".env.sample", ".env.template"}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN " + r"(?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_" + r"[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "OpenAI API key": re.compile(r"\bsk-" + r"(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,}\b"),
}
FORBIDDEN_CONTENT_EXTENSIONS = {
    ".aac",
    ".avi",
    ".doc",
    ".docx",
    ".hwp",
    ".hwpx",
    ".m4a",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".ppt",
    ".pptx",
    ".srt",
    ".wav",
    ".zip",
}
TEXT_PATTERNS = {
    "Windows absolute path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
    "private download path": re.compile(r"(?i)(?:downloads[\\/]2026_Fall|_study_workbench|03_recording_stt|05_participants)"),
    "email address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "Korean phone number": re.compile(r"(?<!\d)01[016789][ -]?\d{3,4}[ -]?\d{4}(?!\d)"),
    "student number": re.compile(r"(?<!\d)20\d{2}[#*\d]{5,8}(?!\d)"),
}


def repository_files() -> list[Path]:
    return [ROOT / os.fsdecode(name) for name in git("ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0") if name]


def git(*arguments: str, input: bytes | None = None) -> bytes:
    try:
        return subprocess.run(["git", *arguments], cwd=ROOT, check=True, capture_output=True, input=input).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("Could not inspect Git publication snapshot") from exc


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or not path.suffix or path.name.lower().startswith(".env")


class Snapshot:
    """Read the worktree, index, or a revision without trusting unstaged bytes."""

    def __init__(self, index: bool = False, revision: str | None = None):
        self.blobs: dict[Path, str] | None = None
        self.texts: dict[str, bytes] = {}
        if not index and revision is None:
            self.files = repository_files()
            return
        self.blobs = {}
        raw = git("ls-files", "--stage", "-z") if index else git("ls-tree", "-r", "-z", "--full-tree", revision or "HEAD")
        for record in raw.split(b"\0"):
            if not record:
                continue
            metadata, filename = record.split(b"\t", 1)
            fields = metadata.decode("ascii").split()
            mode, oid, stage = fields if index else (fields[0], fields[2], "0")
            if stage != "0":
                raise RuntimeError("Unmerged files cannot be published")
            if mode not in {"100644", "100755"}:
                raise RuntimeError("Symlinks and submodules cannot be published")
            self.blobs[ROOT / os.fsdecode(filename)] = oid
        self.files = list(self.blobs)
        wanted = list(dict.fromkeys(oid for path, oid in self.blobs.items() if is_text(path)))
        if wanted:
            payload = git("cat-file", "--batch", input=("\n".join(wanted) + "\n").encode("ascii"))
            offset = 0
            for oid in wanted:
                end = payload.index(b"\n", offset)
                header = payload[offset:end].split()
                if len(header) != 3 or header[1] != b"blob":
                    raise RuntimeError("Invalid Git blob response")
                size = int(header[2])
                offset = end + 1
                self.texts[oid] = payload[offset:offset + size]
                offset += size + 1

    def read_text(self, path: Path) -> str:
        if self.blobs is None:
            return path.read_text(encoding="utf-8")
        return self.texts[self.blobs[path]].decode("utf-8")

    def is_file(self, path: Path) -> bool:
        return path in self.blobs if self.blobs is not None else path.is_file()


def validate(*, index: bool = False, revision: str | None = None) -> list[str]:
    errors: list[str] = []
    try:
        snapshot = Snapshot(index, revision)
        policy = json.loads(snapshot.read_text(ROOT / "scripts/public_validation_policy.json"))
        if not isinstance(policy, dict) or not isinstance(policy.get("archived_courses", []), list):
            raise ValueError("invalid validation policy")
        if any(not isinstance(course, str) for course in policy.get("archived_courses", [])):
            raise ValueError("invalid archived course")
        archived = set(policy.get("archived_courses", []))
    except (RuntimeError, OSError, ValueError, KeyError, TypeError) as exc:
        return [f"Cannot inspect publication snapshot or validation policy: {type(exc).__name__}"]
    for path in snapshot.files:
        try:
            relative = path.relative_to(ROOT)
        except ValueError:
            errors.append(f"outside repository: {path}")
            continue

        lowered_parts = {part.lower() for part in relative.parts}
        if lowered_parts & {part.lower() for part in FORBIDDEN_PARTS}:
            errors.append(f"private path is tracked: {relative}")

        name = path.name.lower()
        if name in SENSITIVE_FILENAMES or ((name == ".env" or name.startswith(".env.")) and name not in ENV_TEMPLATES):
            errors.append(f"credential file cannot be published: {relative}")
        if path.suffix.lower() in FORBIDDEN_CONTENT_EXTENSIONS:
            errors.append(f"raw course asset belongs in GitHub Releases, not Pages: {relative}")

        if snapshot.blobs is None:
            try:
                path.resolve().relative_to(ROOT.resolve())
                if path.is_symlink():
                    raise ValueError("symlink")
            except (ValueError, OSError):
                errors.append(f"unsafe repository path: {relative}")
                continue
        if not is_text(path):
            continue
        try:
            text = snapshot.read_text(path)
        except (OSError, UnicodeError, KeyError):
            errors.append(f"cannot read publication text: {relative}")
            continue

        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label} found in {relative}")

        is_pdf_page_cache = len(relative.parts) >= 2 and relative.parts[:2] == ("content", "page_cache")
        if relative.parts and relative.parts[0] == "content" and not is_pdf_page_cache:
            for label, pattern in TEXT_PATTERNS.items():
                if pattern.search(text):
                    errors.append(f"{label} found in {relative}")

        is_lecture = (
            len(relative.parts) >= 5
            and relative.parts[0] == "content"
            and relative.parts[1] == "courses"
            and relative.parts[3] == "lectures"
            and path.suffix.lower() == ".md"
        )
        is_cache_page = is_pdf_page_cache and path.name.startswith("page-") and path.suffix.lower() == ".md"
        metadata: dict[str, object] = {}
        if is_lecture or is_cache_page:
            try:
                metadata, _ = parse_frontmatter(text)
            except ValueError as exc:
                errors.append(f"{exc}: {relative}")
                continue
        if is_lecture:
            if metadata.get("review_status") != "approved":
                errors.append(f"lecture is not approved: {relative}")
            if "draft" in metadata and metadata["draft"] is not False:
                errors.append(f"draft must be boolean false: {relative}")
            is_english_lecture = len(relative.parts) >= 6 and relative.parts[4] == "en"
            if is_english_lecture and metadata.get("lang") != "en":
                errors.append(f"English lecture is missing lang: en: {relative}")
            assets = metadata.get("source_assets") or []
            if not isinstance(assets, list) or any(not isinstance(asset, str) for asset in assets):
                errors.append(f"source_assets must be a list of filenames: {relative}")
                continue
            if relative.parts[2] not in archived:
                errors.extend(f"{error}: {relative}" for error in validate_lecture_note(text, "en" if is_english_lecture else "ko", any(asset.lower().endswith(".pdf") for asset in assets)))

        if is_cache_page:
            for field in ("course", "source_pdf", "source_url", "generated_at"):
                if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                    errors.append(f"page cache is missing '{field}': {relative}")
            if type(metadata.get("pdf_page")) is not int or metadata["pdf_page"] < 1:
                errors.append(f"invalid page-cache page number: {relative}")

    for manifest_path in snapshot.files:
        relative_manifest = manifest_path.relative_to(ROOT)
        if len(relative_manifest.parts) != 5 or relative_manifest.parts[:2] != ("content", "page_cache") or manifest_path.name != "manifest.json":
            continue
        try:
            manifest = json.loads(snapshot.read_text(manifest_path))
            if not isinstance(manifest, dict):
                raise ValueError("manifest must be an object")
        except (OSError, ValueError, KeyError):
            errors.append(f"invalid page-cache manifest: {relative_manifest}")
            continue
        pages = manifest.get("pages")
        total_pages = manifest.get("total_pages")
        if type(total_pages) is not int or total_pages < 1 or not isinstance(pages, list):
            errors.append(f"invalid page count in {relative_manifest}")
            continue
        if len(pages) != total_pages:
            errors.append(f"manifest page count mismatch: {relative_manifest}")
        for expected_page, page in enumerate(pages, start=1):
            if not isinstance(page, dict) or page.get("pdf_page") != expected_page:
                errors.append(f"manifest page sequence mismatch: {relative_manifest} page {expected_page}")
                continue
            for field in ("markdown", "png"):
                cache_path = page.get(field)
                expected_parent = Path("content" if field == "markdown" else "static") / "page_cache" / relative_manifest.parts[2] / relative_manifest.parts[3]
                if not isinstance(cache_path, str) or Path(cache_path).parent != expected_parent or not snapshot.is_file(ROOT / cache_path):
                    errors.append(f"missing or unsafe {field} for {relative_manifest} page {expected_page}")

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--index", action="store_true", help="Validate staged Git blobs")
    group.add_argument("--revision", help="Validate all blobs in a revision or tree")
    args = parser.parse_args()
    errors = validate(index=args.index, revision=args.revision)
    if errors:
        print("Public-content validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Public-content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
