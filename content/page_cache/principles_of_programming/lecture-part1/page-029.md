---
title: "lecture-part1.pdf — page 29"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 29
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 29 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-028) · Page 29 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-030)

![lecture-part1.pdf — page 29](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-029.png)

## Extracted text

```text
Scope of names
ØBlock
 { val t = 0
    def f(x: Int) = t + g(x+1)
    def g(y: Int) = y * y
    val x = f(5)
    val r = {
       val t = 10
       val s = f(5)
       s - t }
    t + r }
 • Block-scoped definitions are only accessible within the block
 • Inner definitions shadow outer ones of the same name
 • Outer definitions are accessible in nested blocks unless shadowed
 • No duplicate definitions allowed in the same block
 • Functions are evaluated under the environment where they are
   defined, not where they are called
```
