---
title: "lecture-part1.pdf — page 66"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 66
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 66 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-065) · Page 66 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-067)

![lecture-part1.pdf — page 66](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-066.png)

## Extracted text

```text
Exception & Handling
class factRangeException(val arg: Int) extends Exception

def fact(n : Int): Int =
  if (n < 0) throw new factRangeException(n)
  else if (n == 0) 1
  else n * fact(n-1)

def foo(n: Int) = fact(n + 10)

try {
  println (fact(3))
  println (foo(-100))
} catch {
  case e : factRangeException => {
    println("fact range error: " + e.arg)
  }
}
```
