from __future__ import annotations

import unittest

from sync_external_course_materials import parse_material_links, render_materials_page


SOURCE_PAGE = "https://csl.snu.ac.kr/courses/4190.307/2026-2/"


class ExternalCourseMaterialTests(unittest.TestCase):
    def test_parser_keeps_only_same_site_topic_pdfs(self) -> None:
        html = """
        <section id="schedule"><table><tbody>
          <tr><td>9/1</td><td><a href="0-overview.pdf">Course overview</a></td><td></td></tr>
          <tr><td>9/3</td><td><a href="1-intro.pdf?download=1">Introduction</a></td>
              <td><a href="https://pages.cs.wisc.edu/OSTEP/intro.pdf">Reading</a></td></tr>
        </tbody></table></section>
        <section id="resources"><a href="other.pdf">Other PDF</a></section>
        """

        links = parse_material_links(html, SOURCE_PAGE)

        self.assertEqual([item.filename for item in links], ["0-overview.pdf", "1-intro.pdf"])
        self.assertEqual(links[1].label, "Introduction")
        self.assertEqual(links[1].source_url, SOURCE_PAGE + "1-intro.pdf")

    def test_parser_fails_closed_when_schedule_has_no_materials(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "No same-site PDF"):
            parse_material_links('<section id="schedule"><table></table></section>', SOURCE_PAGE)

    def test_materials_page_lists_release_and_upstream_links(self) -> None:
        config = {
            "course": "operating_systems",
            "course_title": "운영체제 (Operating Systems)",
            "source_page": SOURCE_PAGE,
            "release_tag": "2026-fall__operating_systems__materials",
        }
        release_assets = [
            {"name": "OSSyllabus.Yeongmun.pdf", "size": 56042},
            {"name": "1-intro.pdf", "size": 859208},
        ]
        managed = [
            {
                "filename": "1-intro.pdf",
                "source_url": SOURCE_PAGE + "1-intro.pdf",
            }
        ]

        page = render_materials_page(
            config,
            release_assets,
            managed,
            "https://example.github.io/hub",
            "owner/hub",
        )

        self.assertIn("OSSyllabus.Yeongmun.pdf", page)
        self.assertIn("[교수 사이트 원본]", page)
        self.assertIn("/page_cache/operating_systems/1-intro/manifest.json", page)


if __name__ == "__main__":
    unittest.main()
