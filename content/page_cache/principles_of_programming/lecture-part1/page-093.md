---
title: "lecture-part1.pdf — page 93"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 93
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 93 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-092) · Page 93 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-094)

![lecture-part1.pdf — page 93](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-093.png)

## Extracted text

```text
Revisit: Solution with Tail Recursion
def find[A](t: BTree[A], x: A) : Boolean = {
  def findIter(ts: MyList[BTree[A]]) : Boolean =
    ts match {
      case MyNil() => false
      case MyCons(Leaf(), tl) => findIter(tl)
      case MyCons(Node(v, _, _), _) if v == x => true
      case MyCons(Node(_,l,r), tl) =>
       findIter(MyCons(l, MyCons(r, tl))) }
  findIter(MyCons(t, MyNil()))
}

def genTree(v: Int, n: Int) : BTree[Int] = {
  def genTreeIter(t: BTree[Int], m : Int) : BTree[Int] =
   if (m == 0) t
   else genTreeIter(Node(v, t, Leaf()), m-1)
  genTreeIter(Leaf(), n)
}

find(genTree(0,10000), 1)
```
