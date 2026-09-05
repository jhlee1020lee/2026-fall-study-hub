---
title: "lecture-part1.pdf — page 70"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 70
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 70 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-069) · Page 70 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-071)

![lecture-part1.pdf — page 70](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-070.png)

## Extracted text

```text
Structural Types (a.k.a. Record Types): Examples
import reflect.Selectable.reflectiveSelectable
def bar (x: Int) = x+1
val foo = new {
  val a = 1+2
  def b = a + 1
  def f(x: Int) = b + x
  val g : Int => Int = bar _
}
foo.b
foo.f(3)
val ff : Int=>Int = foo.f _
def g(x: {val a: Int; def b: Int;
            def f(x:Int): Int; val g: Int => Int}) =
  x.f(3)
g(foo)
```
