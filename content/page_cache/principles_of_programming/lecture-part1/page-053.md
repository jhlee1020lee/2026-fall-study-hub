---
title: "lecture-part1.pdf — page 53"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 53
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 53 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-052) · Page 53 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-054)

![lecture-part1.pdf — page 53](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-053.png)

## Extracted text

```text
(Parameterized) expression vs. (closure) value
 • Functions defined using “def” are not values but parameterized
   expressions.
 • Parameterized expression f can be converted to a value (f _).
 • The compiler often infers and inserts missing conversions
   automatically.
 • Anonymous functions are values.
 • Anonymous functions can be seen as syntactic sugar:
      (x:T)=>e
   is equivalent to
      { def noname(x:T) = e; (noname _) }
   where noname is not used in e.
 • One can even write a recursive anonymous function in this way.
 • Q: what’s the difference between param. exps and function values?
   A: function values are “closures” (ie, param. exp. + env.)
 • Q: how to implement call-by-name?
   A: The argument expression is converted to a closure.
```
