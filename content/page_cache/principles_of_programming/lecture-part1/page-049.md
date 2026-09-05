---
title: "lecture-part1.pdf — page 49"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 49
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 49 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-048) · Page 49 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-050)

![lecture-part1.pdf — page 49](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-049.png)

## Extracted text

```text
Exercise

 def sum(f: Int=>Int, a: Int, b: Int): Int =
   if (a <= b) f(a) + sum(f, a+1, b) else 0

 def product(f: Int=>Int, a: Int, b: Int): Int =
   if (a <= b) f(a) * product(f, a+1, b) else 1

 DRY (Do not Repeat Yourself) using a higher-order function, called
 “mapReduce”.
```
