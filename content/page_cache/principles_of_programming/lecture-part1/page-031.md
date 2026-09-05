---
title: "lecture-part1.pdf — page 31"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 31
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 31 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-030) · Page 31 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-032)

![lecture-part1.pdf — page 31](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-031.png)

## Extracted text

```text
Safety Checking
Safety checking rules out any use of undefined names.
• For “val x = e”,
  all names in “e” should be defined before this definition.
• For “def x = e”,
  all names in “e” should be defined before the next “val” definition.

/* The following code passes the safety checking */
{ def f(x:Int) = g(x)
   def g(x: Int) = 10
   val a = 10
   f(10) }
/* The following code fails at the safety checking */
{ def f(x:Int) = g(x)
   val a = 10
   def g(x: Int) = 10
   f(10) }
```
