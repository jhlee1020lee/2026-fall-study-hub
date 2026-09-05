---
title: "lecture-part1.pdf — page 42"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 42
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 42 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-041) · Page 42 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-043)

![lecture-part1.pdf — page 42](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-042.png)

## Extracted text

```text
Mutual Recursion: Try
{
    def sum(acc: Int, n: Int): Int =
     if (n <= 0) acc else sum2(n + acc, n-1)

    def sum2(acc: Int, n: Int): Int =
     if (n <= 0) acc else sum(2*n + acc, n-1)

    sum(0, 20000) // stack overflow
}
```
