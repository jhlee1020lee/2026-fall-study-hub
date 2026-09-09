import tempfile
import unittest
from pathlib import Path
from prepare_page_cache_build import literal_page, prepare


class LiteralPageTests(unittest.TestCase):
    def page(self, body):
        return '---\ncourse: "principles_of_programming"\npdf_page: 3\n---\n' + body

    def test_generics_and_markup_are_literal_not_html(self):
        body = 'List<List<T>>\n<script>alert(1)</script>\n$x_1$\n[[not a link]]\n'
        result = literal_page(self.page(body))
        self.assertIn('```text\n' + body + '```\n', result)
        self.assertEqual(literal_page(result), result)

    def test_fence_cannot_be_closed_by_slide_text(self):
        result = literal_page(self.page('```\n````\ntext\n'))
        self.assertIn('`````text\n', result)
        self.assertTrue(result.endswith('`````\n'))

    def test_invalid_metadata_fails_closed(self):
        for text in ('ordinary note', '---\ntitle: Not a PDF\n---\nbody'):
            with self.assertRaises(ValueError):
                literal_page(text)

    def test_notes_and_inactive_materials_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = ['content/page_cache/principles_of_programming/lecture-part3/page-001.md',
                     'content/page_cache/operating_systems/lecture/page-001.md',
                     'content/courses/principles_of_programming/lectures/note.md']
            for relative in paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(self.page('List<T>'), encoding='utf-8')
            originals = [(root / p).read_bytes() for p in paths]
            self.assertEqual(prepare(root), 1)
            self.assertEqual(prepare(root), 0)
            for i in (1, 2):
                self.assertEqual((root / paths[i]).read_bytes(), originals[i])
