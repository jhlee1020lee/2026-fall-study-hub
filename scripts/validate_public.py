#!/usr/bin/env python3
"""Fail closed when private course data is about to enter the public site."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

FORBIDDEN_PARTS = {
    "_drafts",
    "_study_workbench",
    "03_recording_stt",
    "05_participants",
    "participants",
    "recordings",
    "private",
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
REQUIRED_LECTURE_HEADINGS = {
    "## 수업 직후 10분 복습",
    "## 이전 강의와의 연결",
    "## 상세 해설",
    "## 능동회상 문제",
    "## 출처와 검증 상태",
}


def repository_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return [ROOT / line for line in result.stdout.splitlines() if line.strip()]
    except (OSError, subprocess.CalledProcessError):
        return [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]


def validate() -> list[str]:
    errors: list[str] = []
    for path in repository_files():
        try:
            relative = path.relative_to(ROOT)
        except ValueError:
            errors.append(f"outside repository: {path}")
            continue

        lowered_parts = {part.lower() for part in relative.parts}
        if lowered_parts & {part.lower() for part in FORBIDDEN_PARTS}:
            errors.append(f"private path is tracked: {relative}")

        if relative.parts and relative.parts[0] == "content" and path.suffix.lower() in FORBIDDEN_CONTENT_EXTENSIONS:
            errors.append(f"raw course asset belongs in GitHub Releases, not Pages: {relative}")

        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".ts", ".tsx", ".py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        if relative.parts and relative.parts[0] == "content":
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
        if is_lecture:
            if not re.search(r"(?m)^review_status:\s*approved\s*$", text):
                errors.append(f"lecture is not approved: {relative}")
            if re.search(r"(?m)^draft:\s*true\s*$", text):
                errors.append(f"draft lecture is publishable: {relative}")
            for heading in sorted(REQUIRED_LECTURE_HEADINGS):
                if heading not in text:
                    errors.append(f"missing '{heading}' in {relative}")

    return sorted(set(errors))


def main() -> int:
    errors = validate()
    if errors:
        print("Public-content validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Public-content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
