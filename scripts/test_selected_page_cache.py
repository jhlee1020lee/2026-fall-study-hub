from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import refresh_page_cache as refresh
import validate_public as public
from selected_page_cache import selected_cache_dirs, validate_selected_manifest


def make_selected(root: Path) -> tuple[Path, dict]:
    manifest = {
        "schema": "selected_page_cache_v1", "schema_version": 1,
        "publication_mode": "selected_pages", "source_pdf_public": False,
        "course": "course", "source_pdf": "lecture.pdf", "source_sha256": "a" * 64,
        "source_url": "https://example.test/hub/courses/course/note#sources",
        "source_url_kind": "lecture_source_description", "generated_at": "2026-09-08T00:00:00Z",
        "total_pages": 29, "selected_pages": [10, 22, 23], "pages": [],
    }
    for number in manifest["selected_pages"]:
        record = {"pdf_page": number}
        frontmatter = {key: manifest[key] for key in (
            "course", "source_pdf", "source_url", "source_url_kind", "generated_at", "source_pdf_public")}
        frontmatter.update(pdf_page=number, publication_approved=True, review_status="approved", draft=False)
        for kind, prefix, suffix in (("markdown", "content", ".md"), ("png", "static", ".png")):
            relative = f"{prefix}/page_cache/course/lecture/page-{number:03}{suffix}"
            data = ("---\n" + "\n".join(f"{key}: {json.dumps(value)}" for key, value in frontmatter.items())
                    + "\n---\n\nSource figure only.\n").encode() if kind == "markdown" else f"png fixture {number}".encode()
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            record[kind], record[kind + "_sha256"] = relative, hashlib.sha256(data).hexdigest()
        manifest["pages"].append(record)
    path = root / "content/page_cache/course/lecture/manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path, manifest


class SelectedPageCacheTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path, self.manifest = make_selected(self.root)
        self.content, self.static = self.root / "content/page_cache", self.root / "static/page_cache"

    def validate(self, manifest=None):
        files = {path.relative_to(self.root).as_posix() for path in self.root.rglob("*") if path.is_file()}
        validate_selected_manifest(manifest or self.manifest, "course", "lecture",
                                   lambda relative: (self.root / relative).read_bytes(), files)

    def test_valid_bounded_cache_survives_real_main_cleanup(self):
        self.validate()
        for root in (self.content, self.static):
            (root / "course/stale").mkdir()
        args = ["refresh_page_cache.py", "--pdf-root", str(self.root / "pdfs"),
                "--content-root", str(self.content), "--static-root", str(self.static),
                "--site-base", "https://example.test/hub"]
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with patch("sys.argv", args), patch.object(refresh, "require_tool", return_value="unused"), \
                patch.object(refresh, "discover_sources", return_value=([], {})), patch("builtins.print"):
            self.assertEqual(refresh.main(), 0)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertFalse((self.content / "course/stale").exists())
        self.assertFalse((self.static / "course/stale").exists())

    def test_selected_cache_is_not_mistaken_for_complete_released_cache(self):
        self.assertFalse(refresh.cache_is_current(self.path, self.static / "course/lecture", "a" * 64))
        self.assertEqual(refresh.preview_only_cache_dirs(self.content, self.static), (set(), set()))
        self.assertEqual(selected_cache_dirs(self.content, self.static),
                         ({self.path.parent.resolve()}, {(self.static / "course/lecture").resolve()}))

    def test_invalid_schema_counts_ranges_sequence_and_paths_are_rejected(self):
        mutations = {
            "schema": lambda m: m.update(schema="other"),
            "schema_bool": lambda m: m.update(schema_version=True),
            "mode": lambda m: m.update(publication_mode="preview_only"),
            "private_source": lambda m: m.update(source_pdf_public=True),
            "course": lambda m: m.update(course="other"),
            "source_path": lambda m: m.update(source_pdf="../lecture.pdf"),
            "source_hash": lambda m: m.update(source_sha256="bad"),
            "source_kind": lambda m: m.update(source_url_kind="pdf_download"),
            "source_url": lambda m: m.update(source_url="file:///private.pdf"),
            "source_credentials": lambda m: m.update(source_url="https://user:password@example.test/"),
            "total_bool": lambda m: m.update(total_pages=True),
            "total_small": lambda m: m.update(total_pages=2),
            "empty": lambda m: m.update(selected_pages=[]),
            "duplicate": lambda m: m.update(selected_pages=[10, 22, 22]),
            "unsorted": lambda m: m.update(selected_pages=[22, 10, 23]),
            "zero": lambda m: m.update(selected_pages=[0, 22, 23]),
            "out_of_range": lambda m: m.update(selected_pages=[10, 22, 30]),
            "bool_page": lambda m: m.update(selected_pages=[True, 22, 23]),
            "all_pages": lambda m: m.update(selected_pages=list(range(1, 30))),
            "missing_entry": lambda m: m["pages"].pop(),
            "sequence": lambda m: m["pages"][0].update(pdf_page=9),
            "entry_bool": lambda m: m["pages"][0].update(pdf_page=True),
            "path_escape": lambda m: m["pages"][0].update(png="../../outside.png"),
            "path_alias": lambda m: m["pages"][0].update(png="static/page_cache/course/lecture/../lecture/page-010.png"),
            "windows_path": lambda m: m["pages"][0].update(png="static\\page_cache\\course\\lecture\\page-010.png"),
            "wrong_name": lambda m: m["pages"][0].update(png="static/page_cache/course/lecture/page-011.png"),
            "missing_hash": lambda m: m["pages"][0].pop("png_sha256"),
        }
        for label, mutation in mutations.items():
            with self.subTest(label=label):
                modified = copy.deepcopy(self.manifest)
                mutation(modified)
                with self.assertRaises(ValueError):
                    self.validate(modified)

    def test_both_markdown_and_binary_hash_drift_are_rejected(self):
        for kind in ("markdown", "png"):
            with self.subTest(kind=kind):
                path = self.root / self.manifest["pages"][0][kind]
                original = path.read_bytes()
                path.write_bytes(original + b" changed")
                with self.assertRaisesRegex(RuntimeError, "hash drift"):
                    selected_cache_dirs(self.content, self.static)
                path.write_bytes(original)

    def test_wrapper_metadata_must_match_even_after_its_hash_is_updated(self):
        path = self.root / self.manifest["pages"][0]["markdown"]
        data = path.read_bytes().replace(b"publication_approved: true", b"publication_approved: false")
        path.write_bytes(data)
        self.manifest["pages"][0]["markdown_sha256"] = hashlib.sha256(data).hexdigest()
        with self.assertRaisesRegex(ValueError, "publication metadata"):
            self.validate()

    def test_missing_and_extra_files_are_rejected(self):
        png = self.root / self.manifest["pages"][0]["png"]
        original = png.read_bytes()
        png.unlink()
        with self.assertRaisesRegex(RuntimeError, "missing or unsafe"):
            selected_cache_dirs(self.content, self.static)
        png.write_bytes(original)
        (self.path.parent / "page-011.md").write_text("not part of this publication", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "unexpected or missing"):
            selected_cache_dirs(self.content, self.static)

    def test_invalid_manifest_stops_main_before_cleanup(self):
        self.manifest["pages"][0]["png_sha256"] = "0" * 64
        self.path.write_text(json.dumps(self.manifest), encoding="utf-8")
        args = ["refresh_page_cache.py", "--pdf-root", str(self.root / "pdfs"),
                "--content-root", str(self.content), "--static-root", str(self.static),
                "--site-base", "https://example.test/hub"]
        with patch("sys.argv", args), patch.object(refresh, "require_tool", return_value="unused"), \
                patch.object(refresh, "discover_sources", return_value=([], {})), \
                patch.object(refresh, "remove_stale_cache_dirs") as cleanup:
            with self.assertRaisesRegex(RuntimeError, "hash drift"):
                refresh.main()
            cleanup.assert_not_called()

    def test_malformed_selected_marker_fails_closed(self):
        for marker in ('"publication_mode":"selected_pages"', '"schema":"selected_page_cache_v1"', '"selected_pages":['):
            with self.subTest(marker=marker):
                self.path.write_text("{" + marker + ",", encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "Cannot safely inspect selected"):
                    selected_cache_dirs(self.content, self.static)

    def test_symlink_components_are_rejected_even_with_matching_bytes(self):
        png = self.root / self.manifest["pages"][0]["png"]
        for marked in (png, png.parent, self.content):
            with self.subTest(marked=str(marked)), patch.object(Path, "is_symlink", lambda path: path == marked):
                with self.assertRaises((RuntimeError, ValueError)):
                    selected_cache_dirs(self.content, self.static)


class SelectedPublicationSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path, self.manifest = make_selected(self.root)
        self.patcher = patch.object(public, "ROOT", self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.git("init", "-q")
        policy = self.root / "scripts/public_validation_policy.json"
        policy.parent.mkdir()
        policy.write_text('{"archived_courses": []}', encoding="utf-8")
        self.git("add", "--", ".")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True).stdout

    def test_selected_manifest_passes_worktree_index_and_revision(self):
        tree = self.git("write-tree").decode().strip()
        self.assertEqual(public.validate(), [])
        self.assertEqual(public.validate(index=True), [])
        self.assertEqual(public.validate(revision=tree), [])

    def test_binary_hash_uses_exact_index_or_revision_not_unstaged_bytes(self):
        tree = self.git("write-tree").decode().strip()
        png = self.root / self.manifest["pages"][0]["png"]
        original = png.read_bytes()
        png.write_bytes(b"unstaged changed image")
        self.assertTrue(any("hash drift" in error for error in public.validate()))
        self.assertEqual(public.validate(index=True), [])
        self.assertEqual(public.validate(revision=tree), [])
        self.git("add", "--", ".")
        bad_tree = self.git("write-tree").decode().strip()
        png.write_bytes(original)
        self.assertEqual(public.validate(), [])
        self.assertTrue(any("hash drift" in error for error in public.validate(index=True)))
        self.assertTrue(any("hash drift" in error for error in public.validate(revision=bad_tree)))

    def test_extra_staged_page_cannot_be_hidden_by_deleting_worktree_file(self):
        path = self.path.parent / "page-011.md"
        path.write_text("unapproved extra", encoding="utf-8")
        self.git("add", "--", ".")
        path.unlink()
        self.assertTrue(any("unexpected or missing" in error for error in public.validate(index=True)))

    def test_legacy_complete_manifest_still_requires_consecutive_complete_pages(self):
        manifest = copy.deepcopy(self.manifest)
        for key in ("schema", "schema_version", "selected_pages", "publication_mode"):
            manifest.pop(key)
        self.path.write_text(json.dumps(manifest), encoding="utf-8")
        errors = public.validate()
        self.assertTrue(any("page count mismatch" in error for error in errors))
        self.assertTrue(any("page sequence mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
