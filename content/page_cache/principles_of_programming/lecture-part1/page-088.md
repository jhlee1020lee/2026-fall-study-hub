---
title: "lecture-part1.pdf — page 88"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 88
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 88 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-087) · Page 88 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-089)

![lecture-part1.pdf — page 88](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-088.png)

## Extracted text

```text
Type Checking and Inference
Ø Type Checking
                  x1:T1, x2:T2, …, xn:Tn ⊢ e : T
  • def f(x: Boolean): Boolean = x > 3
    => Type error
  • def f(x: Int): Boolean = x > 3
    => OK. f: (x: Int)Boolean
Ø Type Inference
                x1:T1, x2:T2, …, xn:Tn ⊢ e : ?
  • def f(x: Int) = x > 3
    => OK by type inference. f: (x: Int)Boolean
  • Too much type inference is not good. Why?

         You can learn how type checking & inference work in
               4190.310 Programming Languages
```
