---
title: "lecture-part1.pdf — page 51"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 51
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 51 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-050) · Page 51 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-052)

![lecture-part1.pdf — page 51](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-051.png)

## Extracted text

```text
Evaluation for functional values
 1: { val t = 0
 2:   val f : Int=>Int = {   // Note: What if using “def f”?
 3:       val t = 10
 4:       def g(x: Int) : Int = x + t
 5:       g _ }
 6:   f(20) }

* Try: Evaluation without Closures
[E0|t=_,f=_],1 ~ 0
[E0|t=0,f=_],2 ~ (x)x+t
   E0::[E1|t=_,g=(x)x+t],3 ~ 10
   E0::[E1|t=10,g=(x)x+t],5 ~ (x)x+t
[E0|t=0,f=(x)x+t],6 ~ f(20) ~ 20
   f(20): E0::[E2|x=20],x+t ~ 20+0 ~ 20
```
