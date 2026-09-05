from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from refresh_page_cache import (
    PdfSource,
    cache_is_current,
    discover_sources,
    filename_identity,
    main,
    pdf_cache_slug,
    preview_only_cache_dirs,
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

    def make_preview(self, root: Path) -> tuple[Path, Path, Path, dict]:
        content = root / "content" / "page_cache"
        static = root / "static" / "page_cache"
        content_dir = content / "course" / "preview"
        static_dir = static / "course" / "preview"
        content_dir.mkdir(parents=True)
        static_dir.mkdir(parents=True)
        (content_dir / "page-001.md").write_text("extracted text", encoding="utf-8")
        (static_dir / "page-001.png").write_bytes(b"png")
        manifest = {
            "course": "course", "source_pdf": "preview.pdf",
            "source_url": "https://example.test/original", "source_sha256": "a" * 64,
            "generated_at": "2026-09-05T00:00:00Z", "total_pages": 1,
            "publication_mode": "preview_only", "source_pdf_public": False,
            "pages": [{"pdf_page": 1,
                       "markdown": "content/page_cache/course/preview/page-001.md",
                       "png": "static/page_cache/course/preview/page-001.png"}],
        }
        path = content_dir / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return content, static, path, manifest

    def test_preview_only_survives_cleanup_but_unmarked_stale_cache_does_not(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            content, static, manifest_path, _ = self.make_preview(Path(temp_name))
            for root in (content, static):
                (root / "course" / "stale").mkdir()
            expected_content, expected_static = preview_only_cache_dirs(content, static)
            self.assertEqual(remove_stale_cache_dirs(content, expected_content), 1)
            self.assertEqual(remove_stale_cache_dirs(static, expected_static), 1)
            self.assertTrue(manifest_path.is_file())
            self.assertTrue((static / "course" / "preview" / "page-001.png").is_file())

    def test_unmarked_manifest_does_not_protect_stale_cache(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            content, static, path, manifest = self.make_preview(Path(temp_name))
            del manifest["publication_mode"]
            path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(preview_only_cache_dirs(content, static), (set(), set()))
            self.assertEqual(remove_stale_cache_dirs(content, set()), 1)
            self.assertEqual(remove_stale_cache_dirs(static, set()), 1)

    def test_invalid_marked_preview_fails_before_any_cleanup(self) -> None:
        mutations = {
            "public_source": lambda value: value.update(source_pdf_public=True),
            "wrong_course": lambda value: value.update(course="other"),
            "bad_count": lambda value: value.update(total_pages=2),
            "bool_count": lambda value: value.update(total_pages=True),
            "bad_number": lambda value: value["pages"][0].update(pdf_page=2),
            "escaping_path": lambda value: value["pages"][0].update(png="../../outside.png"),
            "bad_hash": lambda value: value.update(source_sha256="bad"),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp_name:
                content, static, path, manifest = self.make_preview(Path(temp_name))
                mutate(manifest)
                path.write_text(json.dumps(manifest), encoding="utf-8")
                with self.assertRaises(RuntimeError):
                    preview_only_cache_dirs(content, static)
                self.assertTrue(path.is_file())
                self.assertTrue((static / "course" / "preview" / "page-001.png").is_file())

    def test_preview_requires_both_page_files(self) -> None:
        for missing in ("markdown", "png"):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as temp_name:
                root = Path(temp_name)
                content, static, path, manifest = self.make_preview(root)
                (root / manifest["pages"][0][missing]).unlink()
                with self.assertRaisesRegex(RuntimeError, "missing or unsafe"):
                    preview_only_cache_dirs(content, static)
                self.assertTrue(path.is_file())

    def test_malformed_preview_blocks_cleanup_but_unmarked_manifest_does_not(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            content, static, path, _ = self.make_preview(Path(temp_name))
            path.write_text('{"publication_mode": "preview_only",', encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Cannot safely inspect preview"):
                preview_only_cache_dirs(content, static)
            self.assertTrue(path.is_file())
            path.write_text('{"old":', encoding="utf-8")
            self.assertEqual(preview_only_cache_dirs(content, static), (set(), set()))

    def test_refresh_main_preserves_preview_content_and_images(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            content, static, path, _ = self.make_preview(root)
            (content / "course" / "stale").mkdir()
            (static / "course" / "stale").mkdir()
            args = ["refresh_page_cache.py", "--pdf-root", str(root / "pdfs"),
                    "--content-root", str(content), "--static-root", str(static),
                    "--site-base", "https://example.test/hub"]
            with patch("sys.argv", args), patch("refresh_page_cache.require_tool", return_value="unused"), \
                    patch("refresh_page_cache.discover_sources", return_value=([], {})), patch("builtins.print"):
                self.assertEqual(main(), 0)
            self.assertTrue(path.is_file())
            self.assertTrue((static / "course" / "preview" / "page-001.png").is_file())
            self.assertFalse((content / "course" / "stale").exists())
            self.assertFalse((static / "course" / "stale").exists())

    def test_preview_rejects_page_symlink_outside_its_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            content, static, _, _ = self.make_preview(root)
            outside = root / "outside.png"
            outside.write_bytes(b"outside")
            png = static / "course" / "preview" / "page-001.png"
            png.unlink()
            try:
                png.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("Creating symlinks is not available")
            with self.assertRaisesRegex(RuntimeError, "missing or unsafe"):
                preview_only_cache_dirs(content, static)
            self.assertEqual(outside.read_bytes(), b"outside")


if __name__ == "__main__":
    unittest.main()
