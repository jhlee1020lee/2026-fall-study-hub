---
title: "lecture-part1.pdf — page 71"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 71
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 71 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-070) · Page 71 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-072)

![lecture-part1.pdf — page 71](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-071.png)

## Extracted text

```text
Type Alias
import reflect.Selectable.reflectiveSelectable
type Foo = {val a: Int; def b: Int; def f(x:Int):Int}

val gn = 0
val foo : Foo = new {
  val a = 3
  def b = a + 1
  def f(x: Int) = b + x + gn
}

foo.f(3)

def g(x: Foo) = {
  val gn = 10
  x.f(3)
}
g(foo)
```
