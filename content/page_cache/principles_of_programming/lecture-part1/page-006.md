---
title: "lecture-part1.pdf — page 6"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 6
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 6 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-005) · Page 6 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-007)

![lecture-part1.pdf — page 6](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-006.png)

## Extracted text

```text
Imperative vs. Functional Programming
ØImperative Programming                        sum = 0;
  • Computation by memory reads/writes         i = n;
  • Sequence of read/write operations          while (i > 0) {
  • Repetition by loop                           sum = sum + i;
  • More procedural (ie, describe how to do)     i = i - 1;
  • Easier to write efficient code             }


                                          def sum(n: Int): Int =
ØFunctional Programming                      if (n <= 0)
 • Computation by function application          0
 • Composition of function applications      else
 • Repetition by recursion                      n + sum(n-1)
 • More declarative (ie, describe what to do)
 • Easier to write safe code
```
