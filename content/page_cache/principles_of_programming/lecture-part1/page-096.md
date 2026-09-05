---
title: "lecture-part1.pdf — page 96"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 96
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 96 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-095) · Page 96 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-097)

![lecture-part1.pdf — page 96](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-096.png)

## Extracted text

```text
A Better Way
sealed abstract class BTree[A]
case class Leaf[A]() extends BTree[A]
case class Node[A](value: A, left: BTree[A], right: BTree[A])
  extends BTree[A]

type BSTree[A] = BTree[(Int,A)]

def lookup[A](t: BSTree[A], k: Int) : MyOption[A] =
  ???

def t : BSTree[String] =
  Node((5,"My5"),
    Node((4,"My4"),Node((2,"My2"),Leaf(),Leaf()),Leaf()),
    Node((7,"My7"),Node((6,"My6"),Leaf(),Leaf()),Leaf()))

lookup(t, 7)
```
