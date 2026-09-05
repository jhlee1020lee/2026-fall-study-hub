---
title: "lecture-part1.pdf — page 59"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 59
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 59 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-058) · Page 59 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-060)

![lecture-part1.pdf — page 59](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-059.png)

## Extracted text

```text
Multiple Parameter List
 def sum(f: Int=>Int): (Int,Int)=>Int = {
   def sumF(a: Int, b: Int): Int =
     if (a <= b) f(a) + sumF(a+1, b) else 0
   sumF _
 }

 Or simply:
 def sum(f: Int=>Int)(a: Int, b: Int): Int =
   if (a <= b) f(a) + sum(f)(a+1, b) else 0

 Note that sum(f) is just a parameterized expression.
 (sum(f) _) creates a closure like (sumF _)

 The following code is slightly inefficient. Think about why.
 def sum(f: Int=>Int): (Int,Int)=>Int =
   (a,b) => if (a <= b) f(a) + sum(f)(a+1, b) else 0
```
