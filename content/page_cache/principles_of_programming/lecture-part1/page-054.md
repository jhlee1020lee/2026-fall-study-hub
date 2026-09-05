---
title: "lecture-part1.pdf — page 54"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 54
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 54 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-053) · Page 54 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-055)

![lecture-part1.pdf — page 54](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-054.png)

## Extracted text

```text
Example: call by name with closures
1: { val t = 0
2: def f(x: =>Int) = t + x
3: val r = {
4:     val t = 10
5:     f(t*t) }            // t*t is treated as ()=>t*t
6: r }
ØEvaluation with Closures
[E0|t=_,f=(x:=>Int)t+x,r=_],1 ~ 0
[E0|t=0,f=(x:=>Int)t+x,r=_],3 ~ 100
  E0::[E1|t=_],4 ~ 10
  E0::[E1|t=10],5 ~ f(t*t) ~ 100
  f(t*t): E0::[E2|x=(E1,t*t)],t+x ~ 0+x ~ 0+100 ~ 100
    x: E1,t*t ~ 10*10 ~ 100
[E0|t=0,f=(x)t+x,r=100],6 ~ r ~ 100
```
