"""Structural gates for reviewed textbook chapters; never a semantic review.

All dependency checks use the caller's publication snapshot. This module does
not read local files, register approvals, or reinterpret historical lecture notes.
"""
from __future__ import annotations

import json
import re
from collections.abc import Callable
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import quote

from note_validation import parse_frontmatter

UNIT_LAYOUT = "textbook_unit_v1"
UNIT_KIND = "unit_chapter"
TAIL_HEADINGS = {
    "ko": ("핵심 정리", "확인·연습문제", "출처"),
    "en": ("Key Takeaways", "Recall and Practice", "Sources"),
}
UNIT_PATH = re.compile(r"content/courses/([a-z][a-z0-9_]*)/units/(?:(en)/)?([a-z0-9]+(?:[-_][a-z0-9]+)*)\.md")
LECTURE_SLUG = re.compile(r"courses/([a-z][a-z0-9_]*)/lectures/(?:en/)?([a-z0-9]+(?:[-_][a-z0-9]+)*)")
H2 = re.compile(r"(?m)^ {0,3}##[ \t]+([^\n]+?)[ \t]*(?:[ \t]+#+[ \t]*)?$")
H4 = re.compile(r"(?m)^ {0,3}####[ \t]+([^\n]+?)[ \t]*(?:[ \t]+#+[ \t]*)?$")
QUESTION_ID = re.compile(r"^(?:(?:확인|회상|연습|Recall|Practice|Question)\s+)?([QP]\d{2,})(?:\b|\s|[.:：·—–-])")


def unit_path(relative: str) -> tuple[str, str, str] | None:
    match = UNIT_PATH.fullmatch(relative)
    if not match or match[3] == "index":
        return None
    return match[1], "en" if match[2] else "ko", match[3]


def declares_unit(metadata: dict[str, object]) -> bool:
    return metadata.get("source_kind") == UNIT_KIND or metadata.get("note_layout") == UNIT_LAYOUT


def structural_prose(body: str) -> str:
    """Mask code/comments without moving offsets used for source-bound sections.

    CommonMark permits longer closing fences, tilde fences, and up to three
    leading spaces. Literal example headings/details must never satisfy a gate.
    """
    masked = list(body)
    for match in re.finditer(r"<!--(?:[\s\S]*?-->|[\s\S]*\Z)", body):
        for pos in range(match.start(), match.end()):
            if masked[pos] != "\n":
                masked[pos] = " "
    comment_free = "".join(masked)
    fence: tuple[str, int] | None = None
    offset = 0
    for line in comment_free.splitlines(keepends=True):
        if fence:
            closing = re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}[ \t]*(?:\n)?", line)
            hide = True
            if closing:
                fence = None
        else:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})([^\n]*)", line)
            hide = bool(opening and (opening[1][0] != "`" or "`" not in opening[2]))
            if hide:
                fence = opening[1][0], len(opening[1])
            elif line.startswith(("    ", "\t")):
                hide = True
        if hide:
            for pos in range(offset, offset + len(line)):
                if masked[pos] != "\n":
                    masked[pos] = " "
        offset += len(line)
    return "".join(masked)


def _populated(text: str) -> bool:
    text = re.sub(r"<!--(?:[\s\S]*?-->|[\s\S]*\Z)", "", text)
    text = re.sub(r"(?m)^ {0,3}(?:`{3,}|~{3,})[^\n]*$", "", text)
    text = re.sub(r"<[^>]*>", "", text)
    return bool(text.strip(" \n\r\t#*_`~|:-"))


# CommonMark HTML tag syntax is narrower than HTMLParser's permissive tag
# names. In particular, a comparison such as i<cars.length or a<b이면 must
# not consume the following real </details> while waiting for a greater-than.
_HTML_NAME = r"[A-Za-z][A-Za-z0-9-]*"
_HTML_ATTRIBUTE = r"[A-Za-z_:][A-Za-z0-9_.:-]*(?:\s*=\s*(?:[^\s\"'=<>`]+|'[^']*'|\"[^\"]*\"))?"
_HTML_TAG = re.compile(r"(?:</" + _HTML_NAME + r"\s*>|<" + _HTML_NAME + r"(?:\s+" + _HTML_ATTRIBUTE + r")*\s*/?>)")
_HTML_BLOCK = re.compile(r"^ {0,3}</?(?:address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|param|pre|script|search|section|source|style|summary|table|tbody|td|textarea|tfoot|th|thead|title|tr|track|ul)(?=[\s/>])", re.I)


def _details_markup(prose: str) -> str:
    """Offset-preserving HTML view solely for details structure checks.

    Keep structural_prose's math-preserving contract for the privacy scanner.
    Fenced/indented code and comments were already masked there. Only complete
    HTML tags reach HTMLParser; complete Markdown code/math spans do not.
    Quoted tag attributes are consumed together, never mistaken for new tags.
    """
    visible = [char if char == "\n" else " " for char in prose]
    raw_html = set()
    offset = 0
    in_block = False
    for line in prose.splitlines(keepends=True):
        if not line.strip(): in_block = False
        elif _HTML_BLOCK.match(line): in_block = True
        if in_block: raw_html.update(range(offset, offset + len(line)))
        offset += len(line)

    def escaped(at):
        slashes = 0
        while at and prose[at - 1] == "\\":
            slashes += 1; at -= 1
        return slashes % 2 == 1

    at = 0
    while at < len(prose):
        tag = _HTML_TAG.match(prose, at) if prose[at] == "<" and not escaped(at) else None
        if tag:
            visible[at:tag.end()] = prose[at:tag.end()]
            at = tag.end()
            continue
        char = prose[at]
        if at not in raw_html and char in {"`", "$"} and not escaped(at):
            opening = re.match(re.escape(char) + "+", prose[at:])[0]
            end = at + len(opening)
            # Inline spans cannot cross a paragraph boundary. Display math may
            # span lines; use an actual matching delimiter, never an open tail.
            boundary = re.search(r"\n[ \t]*\n", prose[end:])
            stop = len(prose) if char == "$" and len(opening) >= 2 else (end + boundary.start() if boundary else len(prose))
            for closing in re.finditer(re.escape(char) + "+", prose[end:stop]):
                close = end + closing.start()
                if len(closing[0]) == len(opening) and not escaped(close):
                    at = end + closing.end()
                    break
            else:
                at = end
            continue
        at += 1
    return "".join(visible)


class _Details(HTMLParser):
    def __init__(self, prose: str, original: str):
        super().__init__(convert_charrefs=True)
        self.original = original
        self.offsets = [0]
        self.offsets.extend(match.end() for match in re.finditer("\n", prose))
        self.current: dict[str, object] | None = None
        self.records: list[tuple[int, int]] = []
        self.errors: list[str] = []
        self.feed(_details_markup(prose))
        self.close()
        if self.current is not None:
            self.errors.append("details must have a closing tag")

    def position(self) -> int:
        line, col = self.getpos()
        return self.offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag == "details":
            if self.current is not None:
                self.errors.append("nested details are not supported")
                return
            self.current = {"start": self.position(), "summaries": 0, "summary_start": None, "answer": None}
            if any(name.lower() == "open" for name, _ in attrs):
                self.errors.append("details must be closed by default (no open attribute)")
        elif tag == "summary":
            if self.current is None:
                self.errors.append("summary must be inside details")
                return
            self.current["summaries"] += 1
            self.current["summary_start"] = self.position() + len(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if tag in {"details", "summary"}:
            self.errors.append("details and summary cannot be self-closing")

    def handle_endtag(self, tag):
        if tag == "summary" and self.current is not None:
            start = self.current["summary_start"]
            if start is None or not _populated(self.original[start:self.position()]):
                self.errors.append("details must have a populated summary")
            self.current["answer"] = self.original.index(">", self.position()) + 1
        elif tag == "details":
            if self.current is None:
                self.errors.append("details closing tag has no opening tag")
                return
            answer = self.current["answer"]
            if self.current["summaries"] != 1 or answer is None:
                self.errors.append("details must contain exactly one closed summary")
            elif not _populated(self.original[answer:self.position()]):
                self.errors.append("details must contain a populated answer")
            self.records.append((self.current["start"], self.original.index(">", self.position()) + 1))
            self.current = None


def validate_unit_layout(body: str, language: str) -> list[str]:
    if language not in TAIL_HEADINGS:
        return ["unsupported unit language"]
    errors: list[str] = []
    prose = structural_prose(body)
    headings = list(H2.finditer(prose))
    names = [match[1] for match in headings]
    tail = TAIL_HEADINGS[language]
    if len(names) < 4 or tuple(names[-3:]) != tail or any(name in tail for name in names[:-3]):
        errors.append("textbook_unit_v1 requires concept H2 sections followed exactly by: " + " → ".join(tail))
    else:
        for index, heading in enumerate(headings[-3:], len(headings) - 3):
            stop = headings[index + 1].start() if index + 1 < len(headings) else len(body)
            if not _populated(body[heading.end():stop]):
                errors.append("unit tail section is empty: " + heading[1])
        generic = {"강의 내용과 설명", "강의 흐름과 연결", "핵심 개념", "상세 해설", "Lecture Content and Explanation", "Lecture Flow and Connections", "Core Concepts", "Detailed Explanation"}
        for index, heading in enumerate(headings[:-3]):
            if heading[1] in generic:
                errors.append("unit teaching H2 must name a concept: " + heading[1])
            if not _populated(body[heading.end():headings[index + 1].start()]):
                errors.append("unit teaching section is empty: " + heading[1])
        recall = headings[-2]
        end = headings[-1].start()
        questions = list(H4.finditer(prose, recall.end(), end))
        seen: set[str] = set()
        kinds: set[str] = set()
        for index, question in enumerate(questions):
            identifier = QUESTION_ID.match(question[1])
            if not identifier:
                errors.append("recall H4 must identify a Qxx recall or Pxx synthetic exercise: " + question[1])
                continue
            qid = identifier[1]
            if qid in seen:
                errors.append("duplicate unit question ID: " + qid)
            seen.add(qid)
            kinds.add(qid[0])
            stop = questions[index + 1].start() if index + 1 < len(questions) else end
            block = _Details(prose[question.end():stop], body[question.end():stop])
            if len(block.records) != 1:
                errors.append(qid + " must have exactly one closed, populated details answer")
            if block.records and not _populated(body[question.end():question.end() + block.records[0][0]]):
                errors.append(qid + " must have a question before its answer")
        if kinds != {"Q", "P"}:
            errors.append("unit recall must include ordinary Qxx recalls and Pxx synthetic practice")
    errors.extend(_Details(prose, body).errors)
    return errors


PUBLIC_BASE = "https://jhlee1020lee.github.io/2026-fall-study-hub"
_INLINE_LINK = re.compile(r"\[([^\]\n]+)\]\((https://[^\s()<>]+)\)")


def _image_end(prose: str, start: int) -> int | None:
    """Skip image labels as a whole: nested link syntax becomes alt text.

    Balanced labels/destinations may contain escapes and code spans. Do not
    resume at an inner '[' and mistake a link-shaped image label for a link.
    """
    def balanced(opening: int, left: str, right: str) -> int | None:
        depth = 1
        at = opening + 1
        while at < len(prose):
            char = prose[at]
            if char == "\\":
                at += 2
                continue
            if left == "[" and char == "`":
                token = re.match(r"`+", prose[at:])[0]
                end = at + len(token)
                for closing in re.finditer(r"`+", prose[end:]):
                    if len(closing[0]) == len(token):
                        at = end + closing.end()
                        break
                else:
                    at = end
                continue
            if left == "(" and char in {"'", '"', "<"}:
                closing = ">" if char == "<" else char
                end = at + 1
                while end < len(prose):
                    if prose[end] == "\\":
                        end += 2
                    elif prose[end] == closing:
                        at = end + 1
                        break
                    else:
                        end += 1
                else:
                    at += 1
                continue
            if char == left:
                depth += 1
            elif char == right:
                depth -= 1
                if depth == 0:
                    return at + 1
            at += 1
        return None

    label_end = balanced(start + 1, "[", "]")
    if label_end is None:
        return None
    if label_end < len(prose) and prose[label_end] == "(":
        return balanced(label_end, "(", ")") or label_end
    if label_end < len(prose) and prose[label_end] == "[":
        return balanced(label_end, "[", "]") or label_end
    return label_end


def _markdown_links(text: str) -> list[tuple[str, str, int]]:
    """Read the simple inline links emitted by material lists and unit sources.

    This intentionally accepts a narrow Markdown shape. Code-styled labels
    are fine; a whole link inside code, math, comments or raw HTML is not.
    No reference resolution or filesystem fallback is involved.
    """
    prose = structural_prose(text)
    links: list[tuple[str, str, int]] = []
    raw_html: set[int] = set()
    offset = 0
    in_block = False
    for line in prose.splitlines(keepends=True):
        if not line.strip():
            in_block = False
        elif _HTML_BLOCK.match(line):
            in_block = True
        if in_block:
            raw_html.update(range(offset, offset + len(line)))
        offset += len(line)
    at = 0
    code_tag = None
    while at < len(prose):
        if prose[at] == "\\":
            at += 2
            continue
        tag = _HTML_TAG.match(prose, at) if prose[at] == "<" else None
        if tag:
            name = re.match(r"</?([A-Za-z][A-Za-z0-9-]*)", tag[0])[1].lower()
            if tag[0].startswith("</") and name == code_tag:
                code_tag = None
            elif name in {"code", "pre", "script", "style", "textarea"}:
                code_tag = name
            at = tag.end()
            continue
        if at in raw_html or code_tag:
            at += 1
            continue
        char = prose[at]
        if prose.startswith("![", at):
            image_end = _image_end(prose, at)
            if image_end is not None:
                at = image_end
                continue
        if char in {"`", "$"}:
            token = re.match(re.escape(char) + "+", prose[at:])[0]
            end = at + len(token)
            boundary = re.search(r"\n[ \t]*\n", prose[end:])
            stop = len(prose) if char == "$" and len(token) >= 2 else (end + boundary.start() if boundary else len(prose))
            for closing in re.finditer(re.escape(char) + "+", prose[end:stop]):
                close = end + closing.start()
                preceding = len(prose[:close]) - len(prose[:close].rstrip("\\"))
                if len(closing[0]) == len(token) and preceding % 2 == 0:
                    at = end + closing.end()
                    break
            else:
                at = end
            continue
        link = _INLINE_LINK.match(prose, at) if char == "[" and (not at or prose[at - 1] != "!") else None
        if link:
            links.append((link[1], link[2], at))
            at = link.end()
        else:
            at += 1
    return links


def _direct_pdf_sources(body: str, course: str, assets: list[str], available_paths: set[str],
                        read_text: Callable[[str], str] | None) -> list[str]:
    """Bind direct public PDF links to the caller's exact materials snapshot.

    Manifest provenance/preview flags are historical, not a claim that the
    public URL equals source_url. Actual asset bytes remain a release/live gate.
    """
    prefix = "unit public PDF source requires a clickable page_cache reference or a snapshot-bound direct PDF"
    materials_path = f"content/courses/{course}/materials.md"
    if read_text is None or materials_path not in available_paths:
        return [prefix + ": materials list unavailable"]
    try:
        materials = read_text(materials_path)
    except (OSError, KeyError, ValueError, UnicodeError):
        return [prefix + ": materials list unreadable"]
    listed_links = _markdown_links(materials)
    unit_urls = {url for _, url, _ in _markdown_links(body)}
    manifest_pattern = re.compile(re.escape(PUBLIC_BASE) + r"/page_cache/" + re.escape(course) + r"/([a-zA-Z0-9][a-zA-Z0-9_-]*)/manifest\.json")
    errors = []
    for asset in assets:
        expected_url = f"{PUBLIC_BASE}/materials/{course}/{quote(asset, safe='')}"
        matched = False
        for label, url, pos in listed_links:
            # The list names the original asset, including its code-style label.
            code_label = re.fullmatch(r"(`+)(.+?)\1", label)
            name = code_label[2] if code_label else label
            if name != asset or url != expected_url or url not in unit_urls:
                continue
            row_start = materials.rfind("\n", 0, pos) + 1
            row_end = materials.find("\n", pos)
            if row_end < 0:
                row_end = len(materials)
            if not re.match(r" {0,3}[-*+]\s+", materials[row_start:row_end]):
                continue
            for _, manifest_url, manifest_pos in listed_links:
                manifest_match = manifest_pattern.fullmatch(manifest_url)
                if not (row_start <= manifest_pos < row_end and manifest_match):
                    continue
                manifest_path = f"content/page_cache/{course}/{manifest_match[1]}/manifest.json"
                if manifest_path not in available_paths:
                    continue
                try:
                    manifest = json.loads(read_text(manifest_path))
                except (OSError, KeyError, ValueError, UnicodeError):
                    continue
                if (isinstance(manifest, dict) and manifest.get("course") == course
                        and manifest.get("source_pdf") == asset
                        and isinstance(manifest.get("source_sha256"), str)
                        and re.fullmatch(r"[0-9a-f]{64}", manifest["source_sha256"])):
                    matched = True
        if not matched:
            errors.append(prefix + ": " + asset)
    return errors


def validate_unit_chapter(text: str, relative: str, available_paths: set[str],
                          read_text: Callable[[str], str] | None = None) -> list[str]:
    """Validate chapter bytes against canonical paths in this exact snapshot."""
    errors: list[str] = []
    identity = unit_path(relative)
    if identity is None:
        return ["unit chapter must use a canonical non-index units/<unit_id>.md or units/en/<unit_id>.md path"]
    course, language, identifier = identity
    try:
        metadata, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]
    required = {"note_layout": UNIT_LAYOUT, "source_kind": UNIT_KIND, "unit_id": identifier,
                "course": course, "lang": language, "review_status": "approved", "draft": False}
    for field, expected in required.items():
        if metadata.get(field) != expected or (field == "draft" and metadata.get(field) is not False):
            errors.append(f"unit {field} must equal {expected!r}")
    assets = metadata.get("source_assets")
    if not isinstance(assets, list) or any(not isinstance(asset, str) or not asset.strip() or asset in {".", ".."} or re.search(r"[\\/:\x00-\x1f]", asset) for asset in assets):
        errors.append("unit source_assets must be a list of original filenames")
        assets = []
    private = metadata.get("private_source_assets", [])
    if not isinstance(private, list) or any(not isinstance(asset, str) or asset not in assets for asset in private):
        errors.append("unit private_source_assets must be a subset of source_assets")
        private = []
    lectures = metadata.get("source_lectures")
    if not isinstance(lectures, list) or not lectures or any(not isinstance(slug, str) for slug in lectures):
        errors.append("unit source_lectures must be a nonempty list of canonical lecture slugs")
    else:
        if len(set(lectures)) != len(lectures):
            errors.append("unit source_lectures contains duplicate slugs")
        for slug in lectures:
            match = LECTURE_SLUG.fullmatch(slug)
            if not match or match[1] != course or match[2] == "index":
                errors.append("unit source_lectures must name a canonical lecture in the same course: " + slug)
            elif str(PurePosixPath("content") / (slug + ".md")) not in available_paths:
                errors.append("unit source lecture is missing from publication snapshot: " + slug)
    errors.extend(validate_unit_layout(body, language))
    prose = structural_prose(body)
    public_pdfs = [asset for asset in assets if asset.lower().endswith(".pdf") and asset not in private]
    if public_pdfs and not re.search(r"(?:\]\([^\s)]*page_cache/[^\s)]+\)|\[\[[^\]\n]*page_cache/[^\]\n]+\]\])", prose):
        errors.extend(_direct_pdf_sources(body, course, public_pdfs, available_paths, read_text))
    return errors
