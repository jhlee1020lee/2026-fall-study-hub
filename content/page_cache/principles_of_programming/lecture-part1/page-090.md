---
title: "lecture-part1.pdf — page 90"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 90
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 90 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-089) · Page 90 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-091)

![lecture-part1.pdf — page 90](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-090.png)

## Extracted text

```text
Parametric Polymorphism: Functions
ØProblem
  def id1(x: Int): Int = x
  def id2(x: Double): Double = x

  • Can we avoid copy and paste?
  • Polymorphism to the rescue!

ØParametric Polymorphism (a.k.a. For-all Types)
  def id[A](x: A) : A = x
  • The type of id is [A](val x:A)=>A
  • id is a parametric expression.
  • id[T] _ is a value of type T=>T for any type T.
  • Function types do not support polymorphism.
    (E.g.) [A](A=>A) is not a valid function value type.
  [We will learn other kinds of polymorphism later.]
```
