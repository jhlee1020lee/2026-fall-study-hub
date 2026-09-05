---
title: "lecture-part1.pdf — page 60"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 60
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 60 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-059) · Page 60 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-061)

![lecture-part1.pdf — page 60](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-060.png)

## Extracted text

```text
Comparison between Param. Exp vs. Closure
 {
     def sum(f: Int=>Int)(a: Int, b: Int): Int =
      if (a <= b) f(a) + sum(f)(a+1, b) else 0
     def sumLinear = sum((n)=>n) _ // sum((n)=>n) incorrect

     sumLinear(0,100)
 }
 {
     def sum(f: Int => Int): (Int, Int) => Int = {
       def sumF(a: Int, b: Int): Int =
        if (a <= b) f(a) + sumF(a + 1, b) else 0
       sumF _
     }
     def sumLinear = sum((n)=>n) // sum((n)=>n) _ incorrect

     sumLinear(0,100)
 }
```
