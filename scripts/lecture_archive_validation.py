"""Narrow navigation-only exception for seven current-course lecture archives."""
from __future__ import annotations

import re
from datetime import date

from note_validation import parse_frontmatter


COURSES = frozenset({'aging_and_family', 'computer_architecture', 'computer_programming',
                    'discrete_mathematics', 'principles_of_programming', 'system_programming', 'exploring_computing'})
KIND = 'lecture_archive'
LAYOUT = 'dated_lecture_archive_v1'
INTRO = '날짜별 노트는 수업 당시의 설명과 자료 범위를 확인하는 기록입니다. 단원별 본문과 함께 읽고, 자료 기반 복습은 실제 수업 발언·진도와 구분하세요.'
STT_LIMIT = '개인정보를 가린 공개용 사본입니다. 불명확한 발화와 각 파일의 출처 제한을 함께 확인하세요.'
EMPTY_LECTURES = '현재 공개된 날짜별 강의노트가 없습니다.'
EMPTY_STT = '현재 공개된 보정 STT가 없습니다. 녹음 누락 여부를 뜻하지는 않습니다.'
HEADINGS = ('## 날짜별 강의 기록', '## 보정 STT', '## 원자료')


def archive_course(relative: str) -> str | None:
    match = re.fullmatch(r'content/courses/([a-z0-9_]+)/lectures/index\.md', relative)
    return match[1] if match and match[1] in COURSES else None


def declares_archive(metadata: dict) -> bool:
    return metadata.get('source_kind') == KIND or metadata.get('archive_layout') == LAYOUT


def validate_lecture_archive(text: str, relative: str, available: set[str], read_text) -> list[str]:
    """Only the generator's archive structure is eligible, in this exact Snapshot."""
    course = archive_course(relative)
    if course is None:
        return ['lecture archive must use an active-course lectures/index.md path']
    try:
        metadata, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]
    fields = {'title', 'description', 'cssclasses', 'course', 'source_kind', 'archive_layout'}
    if (set(metadata) != fields or metadata.get('course') != course
            or metadata.get('source_kind') != KIND or metadata.get('archive_layout') != LAYOUT
            or metadata.get('cssclasses') != ['unit-index']):
        return ['lecture archive needs exact navigation metadata; lecture approval/layout fields cannot bypass review']
    title = metadata.get('title'); description = metadata.get('description')
    if (not isinstance(title, str) or not title.endswith(' 강의 기록') or not title.removesuffix(' 강의 기록').strip()
            or description != title.removesuffix(' 강의 기록') + ' 날짜별 강의노트와 보정 STT'):
        return ['lecture archive title/description must identify the course archive']
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    headings = [line for line in lines if line.startswith('#')]
    top = [INTRO, f'[[courses/{course}/units/index|단원 목차로 돌아가기]]']
    if tuple(headings) != HEADINGS or lines[:2] != top or lines[2:3] != [HEADINGS[0]]:
        return ['lecture archive must have only the generated introduction and three navigation sections']
    stt_index, material_index = lines.index(HEADINGS[1]), lines.index(HEADINGS[2])
    if lines[stt_index + 1:stt_index + 2] != [STT_LIMIT] or lines[material_index + 1:] != [f'- [[courses/{course}/materials|교수 제공 자료 목록과 다운로드]]']:
        return ['lecture archive source-limit/material navigation differs from its declared layout']
    required_links = {f'content/courses/{course}/units/index.md', f'content/courses/{course}/materials.md'}
    if not required_links <= available:
        return ['lecture archive has a missing unit index or material-list target in publication snapshot']
    lecture_lines = lines[3:stt_index]; stt_lines = lines[stt_index + 2:material_index]
    expected_lectures = {p for p in available if p.startswith(f'content/courses/{course}/lectures/') and p.endswith('.md') and p != relative}
    expected_stt = {p for p in available if p.startswith(f'content/courses/{course}/transcripts/') and p.endswith('.md')}
    seen_lectures, seen_stt, lecture_order, stt_order = set(), set(), [], []
    errors = []
    if lecture_lines == [EMPTY_LECTURES]:
        lecture_lines = []
    if stt_lines == [EMPTY_STT]:
        stt_lines = []
    try:
        for line in lecture_lines:
            parts = line.removeprefix('- ').split(' · ')
            if not line.startswith('- ') or len(parts) < 2:
                raise ValueError('unexpected lecture archive prose')
            day = parts.pop(0); date.fromisoformat(day)
            material_label = parts[0] == '자료 기반 복습'
            if material_label:
                parts.pop(0)
            if not 1 <= len(parts) <= 2:
                raise ValueError('archive row needs one or two language links')
            row_material, languages = False, set()
            row_names = set()
            for link in parts:
                match = re.fullmatch(r'\[\[(courses/' + re.escape(course) + r'/lectures/(en/)?(' + re.escape(day) + r'-[a-z0-9_-]+))\|(한국어|English)\]\]', link)
                if not match:
                    raise ValueError('noncanonical, cross-course or mismatched-date lecture link')
                slug, english, name, label = match.groups(); target = 'content/' + slug + '.md'
                language = 'en' if english else 'ko'
                if label != ('English' if english else '한국어') or language in languages or target in seen_lectures or target not in available:
                    raise ValueError('duplicate, missing or mislabeled lecture archive target')
                source, _ = parse_frontmatter(read_text(target))
                if (source.get('review_status') != 'approved' or source.get('draft', False) is not False
                        or source.get('course') != course or source.get('lang', 'ko') != language or source.get('date') != day):
                    raise ValueError('archive lecture target is not the approved dated source in this snapshot')
                row_material |= (source.get('source_mode') == 'materials_only' or source.get('source_basis') == 'materials_only'
                                 or 'materials-only' in source.get('tags', []) or '-materials-' in name)
                seen_lectures.add(target); languages.add(language); row_names.add(name)
            if len(row_names) != 1 or row_material != material_label:
                raise ValueError('archive language grouping or materials-only label differs from sources')
            lecture_order.append((day, next(iter(row_names))))
        for line in stt_lines:
            match = re.fullmatch(r'- \[\[(courses/' + re.escape(course) + r'/transcripts/(\d{4}-\d{2}-\d{2}))\|\2 보정 STT\]\]', line)
            if not match:
                raise ValueError('noncanonical or mislabeled transcript archive target')
            slug, day = match.groups(); date.fromisoformat(day); target = 'content/' + slug + '.md'
            if target in seen_stt or target not in available:
                raise ValueError('duplicate or missing transcript archive target')
            source, _ = parse_frontmatter(read_text(target))
            if source.get('source_kind') != 'corrected_transcript' or source.get('privacy_redacted') is not True:
                raise ValueError('archive transcript is not a privacy-redacted public derivative')
            seen_stt.add(target); stt_order.append(day)
    except (ValueError, KeyError, OSError, TypeError, UnicodeError) as exc:
        errors.append('invalid lecture archive navigation: ' + str(exc))
    if seen_lectures != expected_lectures or seen_stt != expected_stt:
        errors.append('lecture archive must link every existing course lecture and public STT exactly once')
    if lecture_order != sorted(lecture_order) or stt_order != sorted(stt_order):
        errors.append('lecture archive dates must be ordered chronologically')
    if not expected_lectures and lines[3:stt_index] != [EMPTY_LECTURES]:
        errors.append('empty lecture archive must state its bounded empty state')
    if not expected_stt and lines[stt_index + 2:material_index] != [EMPTY_STT]:
        errors.append('empty STT archive must state its bounded empty state')
    return errors
