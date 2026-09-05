---
title: "lecture-part1.pdf — page 64"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 64
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 64 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-063) · Page 64 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-065)

![lecture-part1.pdf — page 64](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-064.png)

## Extracted text

```text
Solution

def mapReduce(reduce:(Int,Int)=>Int,inival: Int)
              (f: Int=>Int) (a: Int, b: Int): Int = {
  if (a <= b) reduce(f(a),mapReduce(reduce,inival)(f)(a+1,b))
  else inival
}

// need to make a closure since mapReduce is param. code.
def sum = mapReduce((x,y)=>x+y,0) _

// val is better than def. Think about why.
val product = mapReduce((x,y)=>x*y,1) _
```
