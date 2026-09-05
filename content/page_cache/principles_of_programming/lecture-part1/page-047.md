---
title: "lecture-part1.pdf — page 47"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 47
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 47 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-046) · Page 47 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-048)

![lecture-part1.pdf — page 47](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-047.png)

## Extracted text

```text
Examples

 def sum(f: Int=>Int, n: Int): Int =
   if (n <= 0) 0 else f(n) + sum(f, n-1)

 def linear(n: Int) = n
 def square(n: Int) = n * n
 def cube(n: Int) = n * n * n

 def sumLinear(n: Int) = sum(linear, n)
 def sumSquare(n: Int) = sum(square, n)
 def sumCubes(n: Int) = sum(cube, n)
```
