---
title: "lecture-part1.pdf — page 32"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 32
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 32 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-031) · Page 32 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-033)

![lecture-part1.pdf — page 32](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-032.png)

## Extracted text

```text
Evaluation for Blocks
1: { val t = 0                     5: val r = {
2: def f(x: Int) = t + g(x+1)      6: val t = 10
3: def g(y: Int) = y*y             7: val s = f(5)
4: val x = f(5) + 7                8: s - t }
                                   9: t + r }
ØEvaluation with Environment
[E0|t=_,f=_,g=_,x=_ ,r=_ ],1 ~ 0
[E0|t=0,f=(x)t+g(x),g=(y)y*y,x=_ ,r=_ ],4 ~ f(5)+7 ~ 36+7~ 43
  f(5): E0::[E1|x=5],t+g(x+1) ~ 0+g(6) ~ 36
          g(6): E0::[E2|y=6],y*y ~ 6*6 ~ 36
[E0|t=0,f=(x)t+g(x),g=(y)y*y,x=43,r=_ ],5 ~ 26
  5: E0::[E3|t=_ ,s=_ ],6 ~ 10
     E0::[E3|t=10,s=_ ],7 ~ f(5) ~ 36
       f(5): E0::[E4|x=5],t+g(x+1) ~ 0+g(6) ~ 36
               g(6): E0::[E5|y=6],y*y ~ 6*6 ~ 36
     E0::[E3|t=10,s=36],8 ~ s-t ~ 26
[E0|t=0,f=(x)t+g(x),g=(y)y*y,x=43,r=26],9 ~ t+r ~ 26
```
