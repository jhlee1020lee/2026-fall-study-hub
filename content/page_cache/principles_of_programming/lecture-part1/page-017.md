---
title: "lecture-part1.pdf — page 17"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 17
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 17 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-016) · Page 17 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-018)

![lecture-part1.pdf — page 17](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-017.png)

## Extracted text

```text
Evaluation strategy: Call-by-value, Call-by-name

                              f(e1,e2)
ØCall-by-value
  • Evaluate the arguments first, then apply the function to them
ØCall-by-name
  • Just apply the function to its arguments, without evaluating them.

def square (x: Int) = x * x

[cbv]square(1+1) ~ square(2) ~ 2*2 ~ 4

[cbn]square(1+1) ~ (1+1)*(1+1) ~ 2*(1+1) ~ 2*2 ~ 4
```
