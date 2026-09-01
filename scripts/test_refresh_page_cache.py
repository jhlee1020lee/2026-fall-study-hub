from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from refresh_page_cache import (
    PdfSource,
    cache_is_current,
    discover_sources,
    filename_identity,
    pdf_cache_slug,
    remove_stale_cache_dirs,
    write_page_markdown,
)


class PageCacheTests(unittest.TestCase):
    def test_resolves_release_asset_and_adds_manifest_link(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            materials_root = root / "content" / "courses"
            materials = materials_root / "computer_programming" / "materials.md"
            materials.parent.mkdir(parents=True)
            materials.write_text("## 파일\n\n- `1 intro.pdf` · 0.8 MiB\n", encoding="utf-8")
            pdf = root / "pdfs" / "computer_programming" / "1.intro.pdf"
            pdf.parent.mkdir(parents=True)
            pdf.write_bytes(b"pdf")

            sources, updates = discover_sources(pdfs := root / "pdfs", materials_root, "https://example.test/hub")

            self.assertEqual(len(sources), 1)
            self.assertEqual(sources[0].asset_name, "1.intro.pdf")
            self.assertEqual(sources[0].cache_slug, "1.intro")
            self.assertIn("/page_cache/computer_programming/1.intro/manifest.json", updates[materials])
            self.assertEqual(pdfs, root / "pdfs")

    def test_page_markdown_preserves_extracted_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            path = Path(temp_name) / "page-026.md"
            source = PdfSource(
                course="computer_programming",
                label="1 intro.pdf",
                asset_name="1.intro.pdf",
                pdf_path=Path("1.intro.pdf"),
                cache_slug="1.intro",
                source_url="https://example.test/1.intro.pdf",
                manifest_url="https://example.test/manifest.json",
            )
            original = "class Example {\n    int value = 1;\n}"

            write_page_markdown(path, source, 26, "2026-09-01T00:00:00Z", original)

            body = path.read_text(encoding="utf-8").split("---\n", 2)[2].lstrip("\n")
            self.assertEqual(body, original + "\n")

    def test_current_cache_requires_hash_and_both_page_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            content = root / "content"
            static = root / "static"
            content.mkdir()
            static.mkdir()
            (content / "page-001.md").write_text("page", encoding="utf-8")
            (static / "page-001.png").write_bytes(b"png")
            manifest = {
                "source_sha256": "abc",
                "total_pages": 1,
                "pages": [
                    {
                        "markdown": "content/page_cache/course/pdf/page-001.md",
                        "png": "static/page_cache/course/pdf/page-001.png",
                    }
                ],
            }
            manifest_path = content / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            self.assertTrue(cache_is_current(manifest_path, static, "abc"))
            self.assertFalse(cache_is_current(manifest_path, static, "different"))

    def test_stale_cache_cleanup_stays_below_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name) / "page_cache"
            keep = root / "course" / "keep"
            stale = root / "course" / "stale"
            keep.mkdir(parents=True)
            stale.mkdir(parents=True)
            (keep / "manifest.json").write_text("{}", encoding="utf-8")
            (stale / "manifest.json").write_text("{}", encoding="utf-8")

            removed = remove_stale_cache_dirs(root, {keep.resolve()})

            self.assertEqual(removed, 1)
            self.assertTrue(keep.exists())
            self.assertFalse(stale.exists())

    def test_filename_normalization(self) -> None:
        self.assertEqual(filename_identity("1 intro.pdf"), filename_identity("1.intro.pdf"))
        self.assertEqual(pdf_cache_slug("1.intro.pdf"), "1.intro")


if __name__ == "__main__":
    unittest.main()
