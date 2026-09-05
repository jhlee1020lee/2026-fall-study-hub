---
title: "lecture-part1.pdf — page 84"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 84
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 84 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-083) · Page 84 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-085)

![lecture-part1.pdf — page 84](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-084.png)

## Extracted text

```text
Exercise

 Write a function “find(t: BTree, x: Int) : Boolean” that checks whether
 x is in t.

 sealed abstract class BTree
 case class Leaf() extends BTree
 case class Node(value: Int, left: BTree, right: BTree)
   extends BTree
```
