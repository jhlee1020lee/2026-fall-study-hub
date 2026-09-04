from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

import download_release_assets


class DownloadTests(unittest.TestCase):
    def test_no_public_release_is_a_successful_empty_mirror(self):
        with patch("sys.argv", ["download_release_assets.py", "--output", "tmp/unused"]), patch.dict("os.environ", {"GITHUB_REPOSITORY": "owner/repo"}), patch("shutil.which", return_value="gh"), patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, stdout="[]")) as run:
            self.assertEqual(download_release_assets.main(), 0)
            self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
