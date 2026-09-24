from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_public as public
from unit_validation import PUBLIC_BASE, structural_prose, validate_unit_chapter, validate_unit_layout


COURSE = "system_programming"
SLUG = f"courses/{COURSE}/lectures/2026-09-23-lecture-06"
RELATIVE = f"content/courses/{COURSE}/units/memory-layout.md"


def unit(language="ko"):
    tail = ("핵심 정리", "확인·연습문제", "출처") if language == "ko" else ("Key Takeaways", "Recall and Practice", "Sources")
    return (
        "---\ntitle: Memory layout\nnote_layout: textbook_unit_v1\nsource_kind: unit_chapter\n"
        f"unit_id: memory-layout\ncourse: {COURSE}\nlang: {language}\nreview_status: approved\ndraft: false\n"
        f"source_assets: [memory.pptx]\nprivate_source_assets: []\nsource_lectures:\n  - {SLUG}\n---\n"
        "An introduction.\n\n## Memory layout\n\nThe process owns distinct regions. [M01 slide 11]\n\n"
        f"## {tail[0]}\n\nObjects and their addresses differ.\n\n## {tail[1]}\n\n"
        "#### 확인 Q01\n\nWhat does this address identify?\n\n<details><summary>Answer</summary>\nThe object's storage.\n</details>\n\n"
        "#### 연습 P01\n\nSynthetic: calculate the object size under the stated ABI.\n\n"
        "<details><summary>Worked answer</summary>\nFour bytes plus four bytes equals eight bytes.\n</details>\n\n"
        f"## {tail[2]}\n\n[[{SLUG}|Lecture and source information]]\n"
    )


def pdf_sources():
    materials = f"content/courses/{COURSE}/materials.md"
    manifest = f"content/page_cache/{COURSE}/memory/manifest.json"
    url = f"{PUBLIC_BASE}/materials/{COURSE}/memory.pdf"
    files = {
        materials: f"- [`memory.pdf`]({url}) · [manifest]({PUBLIC_BASE}/page_cache/{COURSE}/memory/manifest.json)\n",
        manifest: json.dumps({"course": COURSE, "source_pdf": "memory.pdf", "source_sha256": "a" * 64,
                              "source_url": "https://github.com/instructor/historical-course", "preview_only": True}),
    }
    return materials, manifest, url, files


class DirectPdfSourceTests(unittest.TestCase):
    def setUp(self):
        self.materials, self.manifest, self.url, self.files = pdf_sources()
        self.text = unit().replace("memory.pptx", "memory.pdf") + f"\n[Original PDF]({self.url})\n"

    def validate(self, text=None, files=None, reader=None):
        files = self.files if files is None else files
        return validate_unit_chapter(self.text if text is None else text, RELATIVE,
                                     set(files) | {f"content/{SLUG}.md"}, reader or files.__getitem__)

    def test_snapshot_registered_direct_pdf_accepts_code_label_and_historical_provenance(self):
        self.assertEqual(self.validate(), [])
        self.assertEqual(self.validate(self.text.replace("[Original PDF]", "[`memory.pdf`]")), [])

    def test_all_public_pdfs_need_evidence_private_pdf_is_excluded(self):
        text = self.text.replace("source_assets: [memory.pdf]", "source_assets: [memory.pdf, private.pdf, other.pdf]")
        text = text.replace("private_source_assets: []", "private_source_assets: [private.pdf]")
        errors = self.validate(text)
        self.assertEqual(len(errors), 1)
        self.assertIn("other.pdf", errors[0])
        self.assertEqual(self.validate(text.replace(", other.pdf", "")), [])
        self.assertEqual(self.validate(text + "\n[[page_cache/system_programming/memory/page-001|Existing source branch]]"), [])

    def test_missing_unreadable_or_mismatched_snapshot_fails_closed(self):
        for missing in (self.materials, self.manifest):
            with self.subTest(missing=missing):
                self.assertTrue(self.validate(files={k: v for k, v in self.files.items() if k != missing}))
        for field, value in (("course", "other"), ("source_pdf", "other.pdf"), ("source_sha256", "not-a-hash")):
            files = dict(self.files)
            manifest = json.loads(files[self.manifest]); manifest[field] = value
            files[self.manifest] = json.dumps(manifest)
            with self.subTest(field=field): self.assertTrue(self.validate(files=files))
        for value in ("{invalid", "[]"):
            with self.subTest(value=value): self.assertTrue(self.validate(files={**self.files, self.manifest: value}))
        def unreadable(_): raise OSError("fixture read failure")
        self.assertTrue(self.validate(reader=unreadable))
        self.assertTrue(validate_unit_chapter(self.text, RELATIVE, set(self.files) | {f"content/{SLUG}.md"}))

    def test_url_original_label_and_same_row_manifest_are_exact(self):
        row = self.files[self.materials]
        for bad in (row.replace("`memory.pdf`", "`renamed.pdf`"), row.replace(self.url, self.url + "?copy=1"),
                    row.replace("/materials/system_programming/", "/materials/other/"),
                    row.replace("/page_cache/system_programming/", "/page_cache/other/"),
                    row.replace("/memory/manifest.json", "/../memory/manifest.json"),
                    row.replace(" · ", "\n- "), row.replace("https://jhlee1020lee.github.io", "https://example.test")):
            with self.subTest(row=bad): self.assertTrue(self.validate(files={**self.files, self.materials: bad}))
        self.assertTrue(self.validate(self.text.replace(self.url, self.url + "?copy=1")))

    def test_example_or_commented_links_cannot_supply_a_source(self):
        link = f"[Original PDF]({self.url})"
        for wrapper in ("`{}`", "``{}``", "<!-- {} -->", "```md\n{}\n```", "    {}", "$ {} $",
                        "<code>{}</code>", '<span data-example="{}">text</span>', "<div>\n{}\n</div>", "\\{}", "!{}"):
            with self.subTest(wrapper=wrapper):
                self.assertTrue(self.validate(self.text.replace(link, wrapper.format(link))))
        row = self.files[self.materials]
        for wrapper in ("<!-- {} -->", "```md\n{}\n```", "`{}`", "<div>\n{}\n</div>"):
            with self.subTest(material_wrapper=wrapper):
                self.assertTrue(self.validate(files={**self.files, self.materials: wrapper.format(row.strip())}))

    def test_nested_links_in_image_labels_are_alt_text_not_clickable_pdf_sources(self):
        link = f"[Original PDF]({self.url})"
        images = (
            f"![preview {link}](https://example.org/preview.png)",
            f"![preview [nested {link}]](https://example.org/a(b).png)",
            f"![preview \\] {link}](https://example.org/a\\(b.png)",
            f"![preview `]` {link}](<https://example.org/a(b.png>)",
            f'![preview ``literal `]` `` {link}](https://example.org/p.png "a ) title")',
            f"![preview {link}][image-reference]\n\n[image-reference]: https://example.org/p.png",
        )
        for image in images:
            with self.subTest(image=image):
                self.assertTrue(self.validate(self.text.replace(link, image)))
                # Skipping the image must not hide an independent genuine link.
                self.assertEqual(self.validate(self.text.replace(link, image + "\n\n" + link)), [])
        # The material list's filename link itself cannot be an image label.
        row = self.files[self.materials]
        bad = row.replace(f"[`memory.pdf`]({self.url})", f"![preview [`memory.pdf`]({self.url})](https://example.org/p.png)")
        self.assertTrue(self.validate(files={**self.files, self.materials: bad}))


class UnitStructureTests(unittest.TestCase):
    def validate(self, text=None, relative=RELATIVE, files=None):
        return validate_unit_chapter(text or unit(), relative, {f"content/{SLUG}.md"} if files is None else files)

    def test_valid_korean_and_english_units(self):
        self.assertEqual(self.validate(), [])
        english_path = RELATIVE.replace("/units/", "/units/en/")
        self.assertEqual(self.validate(unit("en"), english_path), [])

    def test_canonical_path_and_bound_frontmatter(self):
        for path in (RELATIVE.replace("memory-layout.md", "index.md"), RELATIVE.replace("/units/", "/units/other/"), RELATIVE.replace("/units/", "/units/../units/")):
            with self.subTest(path=path):
                self.assertTrue(self.validate(relative=path))
        for old, new in (("course: system_programming", "course: other"), ("lang: ko", "lang: en"), ("draft: false", 'draft: "false"'), ("review_status: approved", "review_status: pending"), ("unit_id: memory-layout", "unit_id: other")):
            with self.subTest(new=new):
                self.assertTrue(self.validate(unit().replace(old, new)))

    def test_same_course_canonical_source_slugs_must_exist_in_snapshot(self):
        bad = (SLUG.replace(COURSE, "other"), SLUG + ".md", SLUG + "#section", SLUG.replace("lectures/", "lectures/../lectures/"), SLUG.replace("2026-09-23-lecture-06", "index"), "/" + SLUG, SLUG.replace("/", "\\"))
        for slug in bad:
            with self.subTest(slug=slug):
                self.assertTrue(any("canonical lecture" in e for e in self.validate(unit().replace(SLUG, slug))))
        self.assertTrue(any("publication snapshot" in e for e in self.validate(files=set())))

    def test_metadata_cannot_hide_assets_or_use_source_paths(self):
        self.assertTrue(any("original filenames" in e for e in self.validate(unit().replace("memory.pptx", "../memory.pptx"))))
        self.assertTrue(any("subset" in e for e in self.validate(unit().replace("private_source_assets: []", "private_source_assets: [secret.md]"))))
        pdf = unit().replace("memory.pptx", "memory.pdf")
        self.assertTrue(any("page_cache" in e for e in self.validate(pdf)))
        self.assertEqual(self.validate(pdf + "\n[[page_cache/system_programming/memory/page-001|Source page]]\n"), [])
        self.assertEqual(self.validate(pdf.replace("private_source_assets: []", "private_source_assets: [memory.pdf]")), [])

    def test_exact_tail_and_substantive_concept_sections(self):
        for text in (unit().replace("## 핵심 정리", "## 확인·연습문제"), unit() + "\n## Extra\n", unit().replace("## Memory layout", "## 강의 내용과 설명"), unit().replace("The process owns distinct regions. [M01 slide 11]", " ")):
            with self.subTest(text=text):
                self.assertTrue(self.validate(text))

    def test_code_fences_comments_and_indented_examples_cannot_supply_headings(self):
        body = unit().split("---\n", 2)[2]
        for opening, closing in (("```md", "````"), ("~~~~markdown", "~~~~~"), ("   ```md", "   ```")):
            wrapped = opening + "\n" + body + "\n" + closing
            with self.subTest(opening=opening):
                self.assertTrue(validate_unit_layout(wrapped, "ko"))
                self.assertNotIn("## Memory layout", structural_prose(wrapped))
        self.assertTrue(validate_unit_layout("<!--\n" + body + "\n-->", "ko"))
        self.assertTrue(validate_unit_layout("\n".join("    " + line for line in body.splitlines()), "ko"))

    def test_literal_answer_tags_cannot_satisfy_question(self):
        text = unit().replace("<details><summary>Answer</summary>\nThe object's storage.\n</details>", "```html\n<details><summary>Answer</summary>Example only</details>\n````")
        self.assertTrue(any("Q01 must have" in e for e in self.validate(text)))

    def test_each_question_requires_closed_populated_fold(self):
        for text in (unit().replace("<details>", "<details open>", 1), unit().replace("</details>", "", 1), unit().replace("The object's storage.", "<!-- withheld -->"), unit().replace("<summary>Answer</summary>", "<summary></summary>"), unit().replace("#### 연습 P01", "#### 확인 Q01")):
            with self.subTest(text=text):
                self.assertTrue(self.validate(text))
        code_answer = unit().replace("The object's storage.", "```c\nreturn address;\n```")
        self.assertEqual(self.validate(code_answer), [])
        whitespace_close = unit().replace("</summary>\nThe object's storage.", "</summary   >\n ")
        self.assertTrue(any("populated answer" in e for e in self.validate(whitespace_close)))

    def test_comparisons_code_and_math_cannot_swallow_real_answer_tags(self):
        for literal in ("`i<cars.length` and `j<myNumbers[i].length`", "a<b이면, 0≤p<lengths[s]다.",
                        "$a<b$ and $$r_{i+1}<r_i$$", "``literal ` and i<length``"):
            text = unit().replace("The object's storage.", "\n" + literal + "\n")
            with self.subTest(literal=literal): self.assertEqual(self.validate(text), [])
        self.assertIn("$a<b$", structural_prose("Text $a<b$ is retained for privacy checks."))

    def test_code_or_math_literal_details_cannot_supply_a_real_answer(self):
        answer = "<details><summary>Answer</summary>\nThe object's storage.\n</details>"
        for fake in ("`<details><summary>Answer</summary>Value</details>`",
                     "``<details><summary>Answer</summary>`Value`</details>``",
                     "$<details><summary>Answer</summary>Value</details>$",
                     "$$\n<details><summary>Answer</summary>Value</details>\n$$"):
            with self.subTest(fake=fake):
                self.assertTrue(any("Q01 must have" in e for e in self.validate(unit().replace(answer, fake))))

    def test_real_details_errors_remain_visible_after_literal_masking(self):
        for text in (
            unit().replace("The object's storage.", "\n`i<n` $r_i<r_j$\n\n<details><summary>Nested</summary>Text</details>"),
            unit().replace("</details>", "\n`</details>`", 1),
            unit().replace("</summary>", "", 1),
            unit().replace("<details>", '<details open data-note="`<details>`">', 1),
            unit().replace("The object's storage.", "\nAn unmatched ` opener and $ opener.\n"),
        ):
            with self.subTest(text=text):
                if "unmatched" in text: self.assertEqual(self.validate(text), [])
                else: self.assertTrue(self.validate(text))
        # Backticks are literal text within an HTML summary/block, not a way
        # to conceal actual nested HTML tags from the structural gate.
        text = unit().replace("<summary>Answer</summary>", "<summary>`<details>`Answer</summary>")
        self.assertTrue(any("nested details" in e for e in self.validate(text)))

    def test_tag_attributes_do_not_introduce_fake_answer_tags(self):
        text = unit().replace("<details>", '<details data-example="<details open><summary>fake</summary>" title="a > b">', 1)
        self.assertEqual(self.validate(text), [])


class UnitPublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        patcher = patch.object(public, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.git("init", "-q")
        # Archived fixture avoids manufacturing a complete historical lecture.
        self.policy = {"archived_courses": [COURSE]}
        self.write("scripts/public_validation_policy.json", json.dumps(self.policy))
        self.write(f"content/{SLUG}.md", "---\nreview_status: approved\ndraft: false\nsource_assets: []\n---\nHistorical lecture.\n")
        self.chapter = self.write(RELATIVE, unit())

    def git(self, *args):
        return subprocess.run(["git", "-c", "safe.directory=" + str(self.root), *args], cwd=self.root, capture_output=True, check=True).stdout

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def approve_fixture(self):
        self.policy["reviewed_units"] = {RELATIVE: hashlib.sha256(self.chapter.read_bytes()).hexdigest()}
        self.write("scripts/public_validation_policy.json", json.dumps(self.policy))

    def test_new_hash_and_changed_hash_fail_closed(self):
        self.assertTrue(any("unit is unreviewed" in e for e in public.validate()))
        self.approve_fixture()
        self.assertEqual(public.validate(), [])
        self.chapter.write_text(unit() + "Changed", encoding="utf-8")
        self.assertTrue(any("unit is unreviewed or changed" in e for e in public.validate()))

    def test_reviewed_hash_does_not_skip_privacy_metadata_or_structure(self):
        self.chapter.write_text(unit().replace("draft: false", "draft: true") + "\nstudent@example.test\n", encoding="utf-8")
        self.approve_fixture()
        errors = public.validate()
        self.assertTrue(any("email address" in e for e in errors))
        self.assertTrue(any("unit draft" in e for e in errors))

    def test_exact_closed_source_checked_math_does_not_look_like_a_private_drive(self):
        for expression in public.UNIT_MATH_PATH_LOOKALIKES:
            with self.subTest(expression=expression):
                delimiter = "$$" if "\n" in expression else "$"
                text = unit() + "\n" + delimiter + expression + delimiter + "\n"
                self.chapter.write_text(text, encoding="utf-8")
                self.approve_fixture()
                self.assertEqual(public.validate(), [])

    def test_real_paths_stay_blocked_next_to_or_inside_closed_math(self):
        formula = r"F:\mathbb R^n\to\mathbb R^m"
        for path in (r"C:\Users\student\secret", r"D:\downloads\2026_Fall\private", "C:/Users/student/secret"):
            for text in ("$" + formula + "$ " + path, "$" + formula + " + " + path + "$", "$" + path + "$",
                         "$" + formula + path + "$"):
                with self.subTest(text=text):
                    self.chapter.write_text(unit() + "\n" + text, encoding="utf-8")
                    self.approve_fixture()
                    self.assertTrue(any("path" in error for error in public.validate()))

    def test_unclosed_math_code_unknown_commands_and_plain_text_stay_blocked(self):
        formula = r"F:\mathbb R^n\to\mathbb R^m"
        cases = [formula, "$" + formula, "$$" + formula + "$", r"\$" + formula + "$",
                 "`$" + formula + "$`", "``$" + formula + "$``", "```tex\n$" + formula + "$\n````",
                 "~~~\n$" + formula + "$\n~~~", "    $" + formula + "$", "<code>$" + formula + "$</code>",
                 '<span title="$' + formula + '$">text</span>', "$F:\\arbitrary R\\to R$",
                 "$F:\\mathbbx R\\to\\mathbb R$", "$$" + formula + "\n$C:\\Users\\student$"]
        for text in cases:
            with self.subTest(text=text):
                self.assertTrue(public.contains_windows_path(unit() + "\n" + text, RELATIVE))

    def test_masked_code_or_html_inside_math_cannot_hide_a_real_drive_path(self):
        formula = r"F:\mathbb R^n\to\mathbb R^m"
        for concealed in (r'<span data-path="C:\Users\student">', r'`D:\downloads\secret`',
                          r'<code>C:\Users\student</code>', r'<!-- C:\Users\student -->'):
            text = unit() + "\n$" + formula + " " + concealed + "$\n"
            with self.subTest(concealed=concealed):
                self.chapter.write_text(text, encoding="utf-8")
                self.approve_fixture()
                self.assertTrue(any("Windows absolute path" in error for error in public.validate()))

    def test_math_exception_requires_actual_unit_path_identity_and_layout(self):
        text = unit() + "\n$F:\\mathbb R^n\\to\\mathbb R^m$"
        for changed, path in [(text, RELATIVE.replace("/units/", "/lectures/")),
                              (text.replace("textbook_unit_v1", "content_first_v1"), RELATIVE),
                              (text.replace("unit_id: memory-layout", "unit_id: other"), RELATIVE),
                              (text.replace("source_kind: unit_chapter", "source_kind: lecture"), RELATIVE)]:
            with self.subTest(path=path):
                self.assertTrue(public.contains_windows_path(changed, path))
        # A math-looking metadata value never gets a body exception.
        self.assertTrue(public.contains_windows_path(text.replace("title: Memory layout", r"title: $F:\mathbb R\to\mathbb R$"), RELATIVE))

    def test_index_cannot_masquerade_as_chapter_but_plain_index_is_allowed(self):
        self.chapter.unlink()
        index = RELATIVE.replace("memory-layout.md", "index.md")
        self.write(index, "# Unit index\n\n[[courses/system_programming/index|Course]]\n")
        self.assertEqual(public.validate(), [])
        self.write(index, unit())
        self.assertTrue(any("canonical non-index" in e for e in public.validate()))

    def test_chapter_cannot_escape_into_unrelated_content_path(self):
        self.chapter.unlink()
        self.write("content/concepts/hidden-chapter.md", unit())
        self.assertTrue(any("canonical non-index" in e for e in public.validate()))

    def test_invalid_policy_entries_fail_even_without_a_matching_file(self):
        for entries in ({RELATIVE: "bad"}, {RELATIVE + "/../index.md": "0" * 64}, {RELATIVE: False}, []):
            with self.subTest(entries=entries):
                self.policy["reviewed_units"] = entries
                self.write("scripts/public_validation_policy.json", json.dumps(self.policy))
                self.assertTrue(any("validation policy" in e for e in public.validate()))

    def test_index_and_revision_bind_policy_chapter_and_source_to_same_snapshot(self):
        self.approve_fixture()
        self.git("add", ".")
        tree = self.git("write-tree").decode("ascii").strip()
        # Unstaged deletion and drift must not corrupt the staged/revision audit.
        (self.root / f"content/{SLUG}.md").unlink()
        self.chapter.write_text(unit() + "Changed", encoding="utf-8")
        self.assertTrue(public.validate())
        self.assertEqual(public.validate(index=True), [])
        self.assertEqual(public.validate(revision=tree), [])
        # A source restored only in the worktree cannot satisfy the index/tree.
        self.git("rm", "--cached", "--", f"content/{SLUG}.md")
        self.write(f"content/{SLUG}.md", "---\nreview_status: approved\n---\nHistorical lecture.\n")
        missing_tree = self.git("write-tree").decode("ascii").strip()
        for errors in (public.validate(index=True), public.validate(revision=missing_tree)):
            self.assertTrue(any("missing from publication snapshot" in e for e in errors))

    def test_direct_pdf_callback_reads_materials_and_manifest_from_index_and_revision(self):
        materials, manifest, url, files = pdf_sources()
        page = f"content/page_cache/{COURSE}/memory/page-001.md"
        png = f"static/page_cache/{COURSE}/memory/page-001.png"
        data = json.loads(files[manifest])
        data.update(total_pages=1, pages=[{"pdf_page": 1, "markdown": page, "png": png}])
        files[manifest] = json.dumps(data)
        files[page] = ("---\nreview_status: approved\ndraft: false\n" + f"course: {COURSE}\n"
                       + "source_pdf: memory.pdf\nsource_url: https://example.test/old\ngenerated_at: fixture\npdf_page: 1\n---\nSource.\n")
        files[png] = "fixture image placeholder"
        for path, text in files.items(): self.write(path, text)
        self.write(RELATIVE, unit().replace("memory.pptx", "memory.pdf") + f"\n[PDF]({url})\n")
        self.approve_fixture()
        self.assertEqual(public.validate(), [])
        self.git("add", ".")
        tree = self.git("write-tree").decode("ascii").strip()
        # Both reader targets drift in the worktree; the exact staged snapshots
        # still carry the valid list and source identity.
        self.write(materials, files[materials].replace("memory.pdf", "other.pdf"))
        self.write(manifest, "{}")
        self.assertTrue(public.validate())
        self.assertEqual(public.validate(index=True), [])
        self.assertEqual(public.validate(revision=tree), [])
        # Conversely, restored worktree evidence cannot repair either snapshot.
        self.git("add", materials, manifest)
        invalid_tree = self.git("write-tree").decode("ascii").strip()
        self.write(materials, files[materials])
        self.write(manifest, files[manifest])
        self.assertEqual(public.validate(), [])
        for errors in (public.validate(index=True), public.validate(revision=invalid_tree)):
            self.assertTrue(any("snapshot-bound direct PDF" in error for error in errors))

    def test_unreviewed_unit_is_still_blocked_in_archived_course(self):
        self.assertTrue(any("unit is unreviewed" in e for e in public.validate()))

    def test_worktree_approval_cannot_approve_the_index_or_revision(self):
        self.git("add", ".")
        unreviewed_tree = self.git("write-tree").decode("ascii").strip()
        self.approve_fixture()
        self.assertEqual(public.validate(), [])
        for errors in (public.validate(index=True), public.validate(revision=unreviewed_tree)):
            self.assertTrue(any("unit is unreviewed" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
