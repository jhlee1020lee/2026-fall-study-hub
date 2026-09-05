---
title: "lecture-part1.pdf — page 85"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 85
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 85 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-084) · Page 85 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-086)

![lecture-part1.pdf — page 85](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-085.png)

## Extracted text

```text
Solution
def find(t: BTree, i: Int) : Boolean =
  t match {
    case Leaf() => false
    case Node(n,lt,rt) =>
      i == n || find(lt, i) || find(rt, i)
  }

def t: BTree = Node(5,Node(4,Node(2,Leaf(),Leaf()),Leaf()),
  Node(7,Node(6,Leaf(),Leaf()),Leaf()))
find(t,7),find(t,1)
```
