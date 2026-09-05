---
title: "lecture-part1.pdf — page 48"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 48
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 48 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-047) · Page 48 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-049)

![lecture-part1.pdf — page 48](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-048.png)

## Extracted text

```text
Anonymous Functions
ØAnonymous Functions
  • Syntax
     (x1: T1,...,xn:Tn) => e
     or
     (x1,...,xn) => e

  def sumLinear(n: Int) = sum((x:Int)=>x, n)
  def sumSquare(n: Int) = sum((x:Int)=>x*x, n)
  def sumCubes(n: Int) = sum((x:Int)=>x*x*x, n)

  Or simply

  def sumLinear(n: Int) = sum((x)=>x, n)
  def sumSquare(n: Int) = sum((x)=>x*x, n)
  def sumCubes(n: Int) = sum((x)=>x*x*x, n)
```
