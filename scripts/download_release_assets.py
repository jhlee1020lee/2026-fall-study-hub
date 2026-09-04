from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


MATERIALS_TAG = re.compile(r"^[a-z0-9-]+__(?P<course>[a-z0-9_]+)__materials$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Mirror public course-material releases into GitHub Pages")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if not repository or repository.count("/") != 1:
        raise SystemExit("GITHUB_REPOSITORY must contain owner/repository")

    gh = shutil.which("gh")
    if not gh:
        raise SystemExit("GitHub CLI (gh) was not found")

    result = subprocess.run(
        [gh, "release", "list", "--repo", repository, "--limit", "100", "--json", "tagName,isDraft"],
        check=True,
        capture_output=True,
        text=True,
    )
    releases = json.loads(result.stdout or "[]")
    output_root = args.output.resolve()
    mirrored = 0
    for release in releases:
        if not isinstance(release, dict) or release.get("isDraft"):
            continue
        tag = str(release.get("tagName") or "")
        match = MATERIALS_TAG.fullmatch(tag)
        if not match:
            continue
        course = match.group("course")
        target = (args.output / course).resolve()
        target.relative_to(output_root)
        target.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [gh, "release", "download", tag, "--repo", repository, "--dir", str(target), "--clobber"],
            check=True,
        )
        mirrored += 1

    print(f"Mirrored {mirrored} course-material release(s) into {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
