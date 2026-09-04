from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_links import local_target, validate_links


class LinkTests(unittest.TestCase):
    def test_project_prefix_and_canonical_folder_urls(self):
        base = "https://example.test/hub"
        self.assertEqual(local_target("courses/example/index.html", "../../courses/example/materials", base), "courses/example/materials")
        self.assertEqual(local_target("404.html", "/hub", base), "")
        self.assertEqual(local_target("index.html", "/lost-prefix", base), "../lost-prefix")
        self.assertIsNone(local_target("index.html", "https://external.test/page", base))

    def test_checks_pages_images_and_exact_legacy_exceptions(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "index.html").write_text('<a href="missing">x</a><img src="absent.png"><script src="app.js"></script>', encoding="utf-8")
            (root / "app.js").write_text("", encoding="utf-8")
            policy = {"legacy_link_exceptions": [{"source": "index.html", "target": "missing", "reason": "fixture"}]}
            errors, checked, retained = validate_links(root, "https://example.test/hub", policy)
            self.assertEqual(checked, 3)
            self.assertEqual(retained, 1)
            self.assertEqual(errors, ["index.html: missing target absent.png"])


if __name__ == "__main__":
    unittest.main()
