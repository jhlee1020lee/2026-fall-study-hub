---
title: "lecture-part1.pdf — page 94"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 94
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 94 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-093) · Page 94 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-095)

![lecture-part1.pdf — page 94](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-094.png)

## Extracted text

```text
Exercise
BSTree[A] = Leaf
          | Node of Int * A * BSTree[A] * BSTree[A]
def lookup[A](t: BSTree[A], k: Int) : MyOption[A] =
  ???

def t : BSTree[String] =
  Node(5,"My5",
    Node(4,"My4",Node(2,"My2",Leaf(),Leaf()),Leaf()),
    Node(7,"My7",Node(6,"My6",Leaf(),Leaf()),Leaf()))

lookup(t, 7)
lookup(t, 3)
```
