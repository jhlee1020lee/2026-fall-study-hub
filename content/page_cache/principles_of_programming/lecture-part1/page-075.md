---
title: "lecture-part1.pdf — page 75"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 75
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 75 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-074) · Page 75 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-076)

![lecture-part1.pdf — page 75](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-075.png)

## Extracted text

```text
Algebraic Datatypes In Scala
ØAttr
 sealed abstract class Attr
 case class Name(name: String) extends Attr
 case class Age(age: Int) extends Attr
 case class DOB(year: Int, month: Int, day: Int) extends Attr
 case class Height(height: Double) extends Attr

 val a : Attr = Name("Chulsoo Kim")
 val b : Attr = DOB(2000,3,10)

ØIList
 sealed abstract class IList
 case class INil() extends IList
 case class ICons(hd: Int, tl: IList) extends IList

 val x : IList = ICons(2, ICons(1, INil()))
 def gen(n: Int) : IList =
   if (n <= 0) INil()
   else ICons(n, gen(n-1))
```
