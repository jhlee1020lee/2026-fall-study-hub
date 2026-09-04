from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_public as validator


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patcher = patch.object(validator, "ROOT", self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.git("init", "-q")
        self.write("scripts/public_validation_policy.json", json.dumps({"archived_courses": []}))
        self.git("add", "--", "scripts/public_validation_policy.json")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True).stdout

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_korean_filenames_are_scanned(self):
        self.write("content/concepts/한글 이름.md", "student@example.test")
        self.git("add", "--", "content")
        errors = validator.validate()
        self.assertTrue(any("email address" in error and "한글 이름.md" in error for error in errors))

    def test_unreadable_or_invalid_text_fails_closed(self):
        path = self.write("content/example.md", "safe")
        self.git("add", "--", "content")
        path.unlink()
        self.assertTrue(any("cannot read" in error for error in validator.validate()))
        path.write_bytes(b"\xff\xfe")
        self.assertTrue(any("cannot read" in error for error in validator.validate()))

    def test_body_cannot_approve_pending_metadata(self):
        self.write("content/courses/example/lectures/note.md", "---\nreview_status: pending\ndraft: false\n---\nreview_status: approved\n")
        self.assertTrue(any("lecture is not approved" in error for error in validator.validate()))

    def test_root_credentials_and_raw_files_are_rejected(self):
        self.write(".env", "TOKEN=placeholder")
        self.write("export.pdf", "fixture")
        errors = validator.validate()
        self.assertTrue(any("credential file" in error for error in errors))
        self.assertTrue(any("raw course asset" in error for error in errors))

    def test_realistic_secret_is_detected_outside_content(self):
        self.write("configuration.txt", "ghp_" + "a" * 36)
        self.assertTrue(any("GitHub token" in error for error in validator.validate()))

    def test_index_and_revision_read_staged_bytes_not_worktree(self):
        path = self.write("content/concepts/한글.md", "student@example.test")
        self.git("add", "--", "content")
        tree = self.git("write-tree").decode("ascii").strip()
        path.write_text("safe public note", encoding="utf-8")
        self.assertEqual(validator.validate(), [])
        self.assertTrue(any("email address" in error for error in validator.validate(index=True)))
        self.assertTrue(any("email address" in error for error in validator.validate(revision=tree)))

    def test_staged_env_is_rejected_even_when_ignored(self):
        self.write(".gitignore", ".env\n")
        self.write(".env", "TOKEN=placeholder")
        self.git("add", "--force", "--", ".env")
        self.assertTrue(any("credential file" in error for error in validator.validate(index=True)))

    def test_manifest_cannot_point_outside_cache_directory(self):
        self.write("safe.md", "example")
        manifest = {"pages": [{"pdf_page": 1, "markdown": "safe.md", "png": "safe.md"}], "total_pages": 1}
        self.write("content/page_cache/example/pdf/manifest.json", json.dumps(manifest))
        self.assertTrue(any("unsafe markdown" in error for error in validator.validate()))


if __name__ == "__main__":
    unittest.main()
