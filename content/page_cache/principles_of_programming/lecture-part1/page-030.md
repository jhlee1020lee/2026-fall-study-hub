---
title: "lecture-part1.pdf — page 30"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 30
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 30 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-029) · Page 30 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-031)

![lecture-part1.pdf — page 30](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-030.png)

## Extracted text

```text
Problem
// should be allowed
{
  def f(x:Int) = g(x)
  def g(x: Int) = 10
  val x = f(10)
  x
}

// should not be allowed
{
  def f(x:Int) = g(x)
  val x = f(10)
  def g(x: Int) = 10
  x
}
```
