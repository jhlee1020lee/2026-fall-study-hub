---
title: "lecture-part1.pdf — page 20"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 20
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 20 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-019) · Page 20 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-021)

![lecture-part1.pdf — page 20](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-020.png)

## Extracted text

```text
Scala’s name binding strategy
ØCall-by-value
  • Use “val” (also called “field”) e.g. val x = e
  • Evaluate the expression first, then bind the name to it
ØCall-by-name
  • Use “def” (also called “method”) e.g. def x = e
  • Just bind the name to the expression, without evaluating it
  • Mostly used to define functions

  def a = 1 + 2 + 3
  val a = 1 + 2 + 3 // 6
  def b = loop
  val b = loop

  def f(a: Int, b: Int): Int = a*b - 2
```
