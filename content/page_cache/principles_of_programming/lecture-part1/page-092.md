---
title: "lecture-part1.pdf — page 92"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 92
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 92 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-091) · Page 92 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-093)

![lecture-part1.pdf — page 92](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-092.png)

## Extracted text

```text
Parametric Polymorphism: Datatypes
sealed abstract class MyOption[A]
case class MyNone[A]() extends MyOption[A]
case class MySome[A](some: A) extends MyOption[A]

sealed abstract class MyList[A]
case class MyNil[A]() extends MyList[A]
case class MyCons[A](hd: A, tl: MyList[A]) extends MyList[A]

sealed abstract class BTree[A]
case class Leaf[A]() extends BTree[A]
case class Node[A](value: A, left: BTree[A], right: BTree[A])
extends BTree[A]

def x: MyList[Int] = MyCons(3, MyNil())
def y: MyList[String] = MyCons("abc", MyNil())
```
