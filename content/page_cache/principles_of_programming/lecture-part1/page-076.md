---
title: "lecture-part1.pdf — page 76"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 76
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 76 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-075) · Page 76 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-077)

![lecture-part1.pdf — page 76](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-076.png)

## Extracted text

```text
Exercise

 IOption = INone
         | ISome of Int

 BTree = Leaf
       | Node of Int * BTree * BTree


 sealed abstract class IList
 case class INil() extends IList
 case class ICons(hd: Int, tl: IList) extends IList

 def x : IList = ICons(2, ICons(1, INil()))
```
