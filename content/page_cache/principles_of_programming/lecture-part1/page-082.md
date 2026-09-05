---
title: "lecture-part1.pdf — page 82"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 82
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 82 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-081) · Page 82 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-083)

![lecture-part1.pdf — page 82](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-082.png)

## Extracted text

```text
Pattern Matching on Int
 def factorial(n: Int) : Int =
   n match {
     case 0 => 1
     case _ => n * factorial(n-1)
   }

 def fib(n: Int) : Int =
   n match {
     case 0 | 1 => 1
     case _ => fib(n-1) + fib(n-2)
   }
```
