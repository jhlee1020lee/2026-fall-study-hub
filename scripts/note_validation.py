"""Shared, dependency-free publication checks for the local pipeline and CI.

Frontmatter deliberately supports flat YAML scalars and scalar lists only. Unknown
YAML constructs fail explicitly instead of being interpreted differently by Quartz.
"""
from __future__ import annotations

import json
import re

REQUIRED_HEADINGS = {
    "ko": {"## 수업 직후 10분 복습", "## 이전 강의와의 연결", "## 상세 해설", "## 능동회상 문제", "## 출처와 검증 상태"},
    "en": {"## 10-Minute Review", "## Connection to the Previous Lecture", "## Detailed Explanation", "## Active Recall", "## Sources and Verification"},
}
MIN_DETAILED_CHARS = 8000
MIN_SOURCE_CITATIONS = 12
MIN_ACTIVE_RECALL = 8


def _scalar(value: str) -> object:
    value = value.strip()
    if value.startswith('"'):
        try:
            parsed, end = json.JSONDecoder().raw_decode(value)
        except ValueError as exc:
            raise ValueError("invalid quoted frontmatter value") from exc
        if not isinstance(parsed, str) or value[end:].strip() and not value[end:].lstrip().startswith("#"):
            raise ValueError("invalid quoted frontmatter value")
        return parsed
    if value.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'\s*(?:#.*)?", value)
        if not match:
            raise ValueError("invalid single-quoted frontmatter value")
        return match.group(1).replace("''", "'")
    value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() in {"null", "~"} or not value:
        return None
    if re.fullmatch(r"-?(?:0|[1-9]\d*)", value):
        return int(value)
    if value.startswith(("[", "{", "&", "*", "!", "|", ">")) or ": " in value:
        raise ValueError("unsupported frontmatter YAML construct; use a quoted scalar or scalar list")
    return value


def _value(value: str) -> object:
    value = value.strip()
    if not value.startswith("["):
        return _scalar(value)
    match = re.fullmatch(r"\[(.*)\]\s*(?:#.*)?", value)
    if not match:
        raise ValueError("invalid inline frontmatter list")
    content = match.group(1)
    if not content.strip():
        return []
    items = re.findall(r'''(?:"(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^,])+''', content)
    if ",".join(items) != content:
        raise ValueError("invalid inline frontmatter list")
    return [_scalar(item) for item in items]


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    text = text.removeprefix("\ufeff").replace("\r\n", "\n")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter")
    end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if end is None:
        raise ValueError("unterminated YAML frontmatter")
    metadata: dict[str, object] = {}
    list_key: str | None = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.fullmatch(r" {2}-\s+(.+?)\s*", line.rstrip("\n"))
        if item:
            if list_key is None:
                raise ValueError("frontmatter list has no key")
            if metadata[list_key] is None:
                metadata[list_key] = []
            if not isinstance(metadata[list_key], list):
                raise ValueError("frontmatter key mixes scalar and list values")
            metadata[list_key].append(_scalar(item.group(1)))
            continue
        field = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]+(.*))?\s*", line.rstrip("\n"))
        if not field:
            raise ValueError("unsupported or malformed frontmatter field")
        key, raw = field.group(1), field.group(2) or ""
        if key in metadata:
            raise ValueError(f"duplicate frontmatter key: {key}")
        metadata[key] = _value(raw)
        list_key = key if not raw.strip() else None
    return metadata, "".join(lines[end + 1:])


def validate_lecture_note(text: str, language: str = "ko", require_page_links: bool = False) -> list[str]:
    errors: list[str] = []
    if language not in REQUIRED_HEADINGS:
        return [f"unsupported lecture language: {language}"]
    body = text
    if text.removeprefix("\ufeff").startswith("---"):
        try:
            _, body = parse_frontmatter(text)
        except ValueError as exc:
            return [str(exc)]
    # Literal examples must not satisfy publication gates.
    prose = re.sub(r"(?ms)^([`~]{3,})[^\n]*\n.*?^\1[ \t]*$", "", body)
    prose = re.sub(r"(?s)<!--.*?-->", "", prose)
    headings = {line.strip() for line in prose.splitlines() if line.startswith("## ")}
    for heading in sorted(REQUIRED_HEADINGS[language] - headings):
        errors.append(f"missing '{heading}'")
    if len(text) < MIN_DETAILED_CHARS:
        errors.append(f"상세 노트가 너무 짧습니다: {len(text)} < {MIN_DETAILED_CHARS}자")
    citations = len(re.findall(r"\[(?:STT|M\d{2})[^\]]*\]", prose))
    if citations < MIN_SOURCE_CITATIONS:
        errors.append(f"근거 표시가 부족합니다: {citations} < {MIN_SOURCE_CITATIONS}")
    recall_heading = "## Active Recall" if language == "en" else "## 능동회상 문제"
    recall = re.search(r"(?ms)^" + re.escape(recall_heading) + r"[ \t]*\n(.*?)(?=^## |\Z)", prose)
    answer = "Answer" if language == "en" else "정답"
    recall_count = len(re.findall(r"<details>\s*<summary>" + answer + r"</summary>\s*.+?</details>", recall.group(1) if recall else "", re.S))
    if recall_count < MIN_ACTIVE_RECALL:
        errors.append(f"능동회상 문항이 부족합니다: {recall_count} < {MIN_ACTIVE_RECALL}")
    table = re.compile(r"(?m)^[ \t]*\|[^\r\n]+\|[ \t]*\r?\n[ \t]*\|(?:[ \t]*:?-{3,}:?[ \t]*\|)+[ \t]*$")
    if not table.search(prose):
        errors.append("강의 전체 coverage table이 없습니다")
    if require_page_links and not re.search(r"(?:\]\([^\s)]*page_cache/[^\s)]+\)|\[\[[^\]\n]*page_cache/[^\]\n]+\]\])", prose):
        errors.append("PDF page cache로 이동하는 클릭 가능한 근거 링크가 없습니다")
    return errors
