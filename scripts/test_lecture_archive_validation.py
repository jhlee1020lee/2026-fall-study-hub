from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_public as public
from lecture_archive_validation import (COURSES, EMPTY_LECTURES, EMPTY_STT, HEADINGS, INTRO, STT_LIMIT,
                                        validate_lecture_archive)


def archive(course='system_programming', lecture_lines=None, stt_lines=None):
    return ('---\ntitle: Test 강의 기록\ndescription: Test 날짜별 강의노트와 보정 STT\ncssclasses: [unit-index]\n'
            f'course: {course}\nsource_kind: lecture_archive\narchive_layout: dated_lecture_archive_v1\n---\n\n'
            + INTRO + f'\n\n[[courses/{course}/units/index|단원 목차로 돌아가기]]\n\n' + HEADINGS[0] + '\n\n'
            + ('\n'.join(lecture_lines) if lecture_lines is not None else EMPTY_LECTURES) + '\n\n' + HEADINGS[1] + '\n\n'
            + STT_LIMIT + '\n\n' + ('\n'.join(stt_lines) if stt_lines is not None else EMPTY_STT) + '\n\n' + HEADINGS[2]
            + f'\n\n- [[courses/{course}/materials|교수 제공 자료 목록과 다운로드]]\n')


class ArchiveStructureTests(unittest.TestCase):
    def validate(self, text=None, course='system_programming', sources=None, path=None):
        files = {f'content/courses/{course}/units/index.md': '# Units', f'content/courses/{course}/materials.md': '# Materials', **(sources or {})}
        return validate_lecture_archive(text or archive(course), path or f'content/courses/{course}/lectures/index.md', set(files), files.__getitem__)

    def note(self, lang='ko', materials=False):
        return (f'---\ncourse: system_programming\ndate: 2026-09-01\nlang: {lang}\nreview_status: approved\ndraft: false\n'
                + ('source_basis: materials_only\n' if materials else '') + '---\nExisting historical note.\n')

    def test_seven_exact_empty_course_archives_pass(self):
        for course in COURSES:
            with self.subTest(course=course): self.assertEqual(self.validate(course=course), [])

    def test_grouped_languages_materials_and_public_stt_pass(self):
        ko = 'courses/system_programming/lectures/2026-09-01-lecture-01'
        en = 'courses/system_programming/lectures/en/2026-09-01-lecture-01'
        stt = 'courses/system_programming/transcripts/2026-09-01'
        sources = {'content/' + ko + '.md': self.note(materials=True), 'content/' + en + '.md': self.note('en', True),
                   'content/' + stt + '.md': '---\nsource_kind: corrected_transcript\nprivacy_redacted: true\n---\nTranscript.'}
        text = archive(lecture_lines=[f'- 2026-09-01 · 자료 기반 복습 · [[{ko}|한국어]] · [[{en}|English]]'],
                       stt_lines=[f'- [[{stt}|2026-09-01 보정 STT]]'])
        self.assertEqual(self.validate(text, sources=sources), [])
        self.assertTrue(self.validate(text.replace(' · 자료 기반 복습', ''), sources=sources))

    def test_archive_cannot_hide_lecture_approval_or_arbitrary_teaching(self):
        invalid = (archive().replace('source_kind: lecture_archive', 'source_kind: lecture_archive\nreview_status: approved\ndraft: false'),
                   archive().replace('source_kind: lecture_archive', 'source_kind: lecture'),
                   archive().replace(INTRO, 'New lecture explanation that bypasses approval.'),
                   archive() + '\n## A new lecture topic\nUnreviewed teaching.',
                   archive().replace(EMPTY_LECTURES, '```\n' + EMPTY_LECTURES + '\n```'),
                   archive().replace(EMPTY_STT, 'No transcripts; perhaps they were not recorded.'))
        for text in invalid:
            with self.subTest(text=text): self.assertTrue(self.validate(text))

    def test_markers_cannot_exempt_arbitrary_or_inactive_paths(self):
        for path in ('content/courses/system_programming/lectures/draft.md',
                     'content/courses/system_programming/lectures/en/index.md',
                     'content/courses/operating_systems/lectures/index.md', 'content/concepts/index.md'):
            with self.subTest(path=path): self.assertTrue(self.validate(path=path))

    def test_source_completeness_date_language_and_approval_are_checked(self):
        slug = 'courses/system_programming/lectures/2026-09-01-lecture-01'
        sources = {'content/' + slug + '.md': self.note()}
        text = archive(lecture_lines=[f'- 2026-09-01 · [[{slug}|한국어]]'])
        self.assertEqual(self.validate(text, sources=sources), [])
        self.assertTrue(self.validate(sources=sources))
        for wrong in (text.replace('|한국어', '|English'), text.replace('- 2026-09-01 ·', '- 2026-09-02 ·'),
                      text.replace(slug, slug.replace('system_programming', 'computer_programming'))):
            with self.subTest(wrong=wrong): self.assertTrue(self.validate(wrong, sources=sources))
        for replacement in ('pending', 'draft'):
            self.assertTrue(self.validate(text, sources={next(iter(sources)): self.note().replace('approved', replacement)}))

    def test_same_snapshot_targets_and_no_duplicate_rows(self):
        slug = 'courses/system_programming/lectures/2026-09-01-lecture-01'
        line = f'- 2026-09-01 · [[{slug}|한국어]]'
        self.assertTrue(self.validate(archive(lecture_lines=[line])))
        self.assertTrue(self.validate(archive(lecture_lines=[line, line]), sources={'content/' + slug + '.md': self.note()}))
        text = archive()
        self.assertTrue(validate_lecture_archive(text, 'content/courses/system_programming/lectures/index.md', set(), lambda _: ''))


class ArchiveSnapshotTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup); self.root = Path(temp.name)
        self.patch = patch.object(public, 'ROOT', self.root); self.patch.start(); self.addCleanup(self.patch.stop)
        self.git('init', '-q')
        self.write('scripts/public_validation_policy.json', json.dumps({'archived_courses': []}))
        self.write('content/courses/system_programming/units/index.md', '# Units')
        self.write('content/courses/system_programming/materials.md', '# Materials')
        self.archive = self.write('content/courses/system_programming/lectures/index.md', archive())

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True).stdout

    def write(self, relative, text):
        path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding='utf-8', newline='\n'); return path

    def test_valid_archive_is_exempted_but_actual_pending_lecture_is_not(self):
        self.assertEqual(public.validate(), [])
        self.write('content/courses/system_programming/lectures/2026-09-01-lecture-01.md',
                   '---\nreview_status: pending\ndraft: true\n---\nUnapproved lecture.')
        errors = public.validate()
        self.assertTrue(any('lecture is not approved' in error for error in errors))
        self.assertTrue(any('every existing course lecture' in error for error in errors))

    def test_index_and_revision_use_actual_snapshot_targets_not_disk(self):
        self.git('add', '--', '.'); tree = self.git('write-tree').decode().strip()
        (self.root / 'content/courses/system_programming/units/index.md').unlink()
        self.assertEqual(public.validate(index=True), [])
        self.assertEqual(public.validate(revision=tree), [])
        self.assertTrue(any('publication snapshot' in error for error in public.validate()))

    def test_malformed_index_is_not_a_lecture_bypass(self):
        self.archive.write_text(archive().replace(INTRO, 'Unchecked lecture text.'), encoding='utf-8')
        errors = public.validate()
        self.assertTrue(any('three navigation sections' in error for error in errors))
        self.assertTrue(any('lecture is not approved' in error for error in errors))


if __name__ == '__main__':
    unittest.main()
