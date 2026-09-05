---
title: "lecture-part1.pdf — page 19"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 19
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 19 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-018) · Page 19 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-020)

![lecture-part1.pdf — page 19](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-019.png)

## Extracted text

```text
Scala’s evaluation strategy
ØCall-by-value
  • By default
ØCall-by-name
  • Use “=>”

  def one(x: Int, y: =>Int) = 1

  one(1+2, loop)

  one(loop, 1+2)
```
