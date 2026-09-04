from __future__ import annotations

import unittest

from note_validation import parse_frontmatter, validate_lecture_note


class FrontmatterTests(unittest.TestCase):
    def test_reads_metadata_not_body(self):
        metadata, body = parse_frontmatter('---\nreview_status: pending\ndraft: false\nsource_assets:\n  - "lecture.pdf"\ntags: [course, "two words"]\n---\nreview_status: approved\n')
        self.assertEqual(metadata["review_status"], "pending")
        self.assertIs(metadata["draft"], False)
        self.assertEqual(metadata["source_assets"], ["lecture.pdf"])
        self.assertEqual(metadata["tags"], ["course", "two words"])
        self.assertIn("approved", body)

    def test_duplicate_malformed_and_aliased_yaml_fail(self):
        for text in ('---\nreview_status: pending\nreview_status: approved\n---\n', '---\ndraft: false\n', '---\nreview_status: &ok approved\n---\n', '---\ndraft: {value: false}\n---\n'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_frontmatter(text)

    def test_quotes_comments_and_empty_list(self):
        metadata, _ = parse_frontmatter('---\ntitle: "a: b # c" # comment\nconcepts: []\ndraft: "false"\n---\n')
        self.assertEqual(metadata["title"], "a: b # c")
        self.assertEqual(metadata["concepts"], [])
        self.assertEqual(metadata["draft"], "false")

    def test_quality_does_not_count_examples_as_requirements(self):
        text = '```md\n## 능동회상 문제\n' + '<details><summary>정답</summary>answer</details>\n' * 8 + '```\n' + 'x' * 8000
        errors = validate_lecture_note(text)
        self.assertTrue(any("0 < 8" in error for error in errors))
        self.assertTrue(any("missing '## 능동회상 문제'" in error for error in errors))

    def test_pdf_link_must_be_clickable(self):
        errors = validate_lecture_note('page_cache/course/pdf/page-001', require_page_links=True)
        self.assertTrue(any("클릭 가능한" in error for error in errors))
        errors = validate_lecture_note('[page](https://example.test/page_cache/course/pdf/page-001)', require_page_links=True)
        self.assertFalse(any("클릭 가능한" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
