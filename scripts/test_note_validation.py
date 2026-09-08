from __future__ import annotations

import unittest

from note_validation import (CONTENT_FIRST_HEADINGS, parse_frontmatter,
                             validate_content_first_layout, validate_lecture_note)


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

    def test_content_first_layout_is_ordered_not_a_heading_set(self):
        for language, names in CONTENT_FIRST_HEADINGS.items():
            body = "\n\n".join("## " + name + "\n\ntext" for name in names)
            with self.subTest(language=language):
                self.assertEqual(validate_content_first_layout(body, language), [])
                swapped = list(names)
                swapped[1], swapped[2] = swapped[2], swapped[1]
                self.assertTrue(validate_content_first_layout("\n\n".join("## " + n + "\n\ntext" for n in swapped), language))
                self.assertTrue(validate_content_first_layout(body + "\n\n## " + names[0] + "\n", language))

    def test_tagged_legacy_cannot_fall_back_and_old_buckets_are_not_integration(self):
        legacy = "---\nnote_layout: content_first_v1\n---\n## 상세 해설\n\nold"
        self.assertTrue(any("content_first_v1" in e for e in validate_lecture_note(legacy)))
        body = "\n\n".join("## " + name + "\n\ntext" for name in CONTENT_FIRST_HEADINGS["ko"])
        self.assertTrue(validate_content_first_layout(body.replace("## 강의 내용과 설명\n", "## 강의 내용과 설명\n\n### 상세 해설\n")))

    def test_new_recall_is_counted_and_alias_anchors_are_preserved(self):
        body = "\n\n".join("## " + name + "\n\ntext" for name in CONTENT_FIRST_HEADINGS["ko"])
        body = body.replace("## 회상·연습문제\n", "## 회상·연습문제\n\n<a id=\"능동회상-문제\"></a>\n\n" +
                            "\n\n".join("<details><summary>정답</summary>worked answer</details>" for _ in range(8)))
        self.assertFalse(any("문항이 부족" in e for e in validate_lecture_note(body)))


if __name__ == "__main__":
    unittest.main()
