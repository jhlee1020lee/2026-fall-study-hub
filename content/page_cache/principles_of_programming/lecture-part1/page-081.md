---
title: "lecture-part1.pdf — page 81"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 81
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 81 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-080) · Page 81 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-082)

![lecture-part1.pdf — page 81](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-081.png)

## Extracted text

```text
Advanced Pattern Matching: An Example
 def secondElmt(xs: IList) : IOption =
   xs match {
     case INil() | ICons(_,INil()) => INone()
     case ICons(_, ICons(x, _)) => ISome(x)
   }
 Vs.
 def secondElmt2(xs: IList) : IOption =
   xs match {
     case INil() | ICons(_,INil()) => INone()
     case ICons(_, ICons(x, INil())) => ISome(x)
     case _ => INone()
   }
 Vs.
 def secondElmt2(xs: IList) : IOption =
   xs match {
     case ICons(_, ICons(x, INil())) => ISome(x)
     case _ => INone() }
```
