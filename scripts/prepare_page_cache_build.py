"""Quote verbatim PDF extracts only in the disposable CI build checkout.

Committed extracts, PDFs, manifests, hashes and lecture notes remain unchanged.
Untrusted slide syntax must not become HTML tags, executable markup or Markdown.
"""
from pathlib import Path
import re

ACTIVE = {"aging_and_family", "computer_architecture", "computer_programming",
          "discrete_mathematics", "principles_of_programming", "system_programming"}


def literal_page(text: str) -> str:
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError("PDF cache page lacks complete frontmatter")
    metadata, body = match.groups()
    if re.search(r"(?m)^page_cache_literal_build: true$", metadata):
        return text
    if not re.search(r"(?m)^pdf_page: [1-9][0-9]*$", metadata):
        raise ValueError("Expected a PDF source page")
    longest = max((len(run) for run in re.findall(r"`+", body)), default=0)
    fence = "`" * max(3, longest + 1)
    return ("---\n" + metadata + "\npage_cache_literal_build: true\n---\n\n"
            + fence + "text\n" + body + ("" if body.endswith("\n") else "\n") + fence + "\n")


def prepare(root: Path) -> int:
    count = 0
    for course in sorted(ACTIVE):
        for page in sorted((root / "content/page_cache" / course).glob("*/page-*.md")):
            if page.is_symlink() or not page.resolve().is_relative_to(root.resolve()):
                raise ValueError("PDF cache build path escaped checkout")
            original = page.read_text(encoding="utf-8")
            quoted = literal_page(original)
            if quoted != original:
                page.write_text(quoted, encoding="utf-8", newline="\n")
                count += 1
    return count


if __name__ == "__main__":
    print(f"Prepared {prepare(Path.cwd())} literal PDF text pages in disposable build checkout.")
