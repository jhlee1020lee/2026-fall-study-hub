---
title: "lecture-part1.pdf — page 43"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 43
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 43 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-042) · Page 43 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-044)

![lecture-part1.pdf — page 43](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-043.png)

## Extracted text

```text
Mutual Recursion: Tail Call Optimization
import scala.util.control.TailCalls._

{
    def sum(acc: Int, n: Int): TailRec[Int] =
     if (n <= 0) done(acc) else tailcall(sum2(n + acc, n-1))

    def sum2(acc: Int, n: Int): TailRec[Int] =
     if (n <= 0) done(acc) else tailcall(sum(2*n + acc, n-1))

    sum(0, 20000).result
}
```
