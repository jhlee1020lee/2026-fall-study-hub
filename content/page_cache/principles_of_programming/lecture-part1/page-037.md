---
title: "lecture-part1.pdf — page 37"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 37
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 37 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-036) · Page 37 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-038)

![lecture-part1.pdf — page 37](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-037.png)

## Extracted text

```text
Lazy call-by-value
ØLazy call-by-value
  • Use “lazy val”    e.g. lazy val x = e
  • Evaluate the expression first time it is used, then bind the name to it

  def f(c: Boolean, i: =>Int): Int = {
    lazy val iv = i
    if (c) 0
    else iv * iv * iv
  }

  f(true, {println("ok"); 100+100+100+100})
  f(false, {println("ok"); 100+100+100+100})
```
