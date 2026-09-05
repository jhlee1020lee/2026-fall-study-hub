---
title: "lecture-part1.pdf — page 72"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 72
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 72 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-071) · Page 72 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-073)

![lecture-part1.pdf — page 72](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-072.png)

## Extracted text

```text
Structural Types: Evaluation
1: def bar (x: Int) = x+1
2: val foo = new //or, object foo
3: { val a = 2 + 1
4: def f(x: Int) = a + x
5: val g : Int => Int = bar _
6: }
7: val b = foo.f(1)
8: foo.g(b)
ØEvaluation with Closures
E1[],1 ~ E1[bar=(x)x+1],2 ~ E1[…]:E2[],3 ~
E1[…]:E2[a=3],4 ~
E1[…]:E2[a=3,f=(x)a+x],5 ~
E1[…]:E2[a=3,f=(x)a+x,g=((x)x+1,E1)],6 ~
E1[bar=(x)x+1,foo=(E2)],7 ~
E1[bar=(x)x+1,foo=(E2),b=4],8 ~ 5
7: E1:E2:E3[x=1],a+x ~ 3+1 ~ 4
8: E1:E4[x=4],x+1 ~ 4+1 ~ 5
```
