---
title: "lecture-part1.pdf — page 57"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 57
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 57 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-056) · Page 57 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-058)

![lecture-part1.pdf — page 57](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-057.png)

## Extracted text

```text
Solution

 def sum(f: Int=>Int): (Int,Int)=>Int = {
   def sumF(a: Int, b: Int): Int =
     if (a <= b) f(a) + sumF(a+1, b) else 0
   sumF // sumF _
 }

 def sumLinear = sum((n)=>n)
 def sumSquare = sum((n)=>n*n)
 def sumCubes = sum((n)=>n*n*n)
```
