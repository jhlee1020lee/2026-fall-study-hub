---
title: "lecture-part1.pdf — page 80"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 80
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 80 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-079) · Page 80 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-081)

![lecture-part1.pdf — page 80](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-080.png)

## Extracted text

```text
Advanced Pattern Matching
Ø Advanced Pattern Matching
  e match {
      case P1 => e1
       …
      case Pn => en
  }
  • One can combine constructors and use _ and | in a pattern.
    (E.g) case ICons(x, INil()) | ICons(x, ICons(_, INil())) => …
  • The given value e is matched against the first pattern P1.
    If succeeds, evaluate e1.
    If fails, e is matched against P2.
    If succeeds, evaluate e2.
    If fails, …
  • The compiler checks exhaustiveness (ie, whether there is a missing
    case).
```
