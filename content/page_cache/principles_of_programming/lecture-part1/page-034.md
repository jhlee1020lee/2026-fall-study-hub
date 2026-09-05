---
title: "lecture-part1.pdf — page 34"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 34
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 34 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-033) · Page 34 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-035)

![lecture-part1.pdf — page 34](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-034.png)

## Extracted text

```text
Exercise: Writing Better Code using Blocks
ØMake the following code better
def isGoodEnough(guess: Double, x: Double) =
  guess*guess/x > 0.999 && guess*guess/x < 1.001

def improve(guess: Double, x: Double) =
  (guess + x/guess) / 2

def sqrtIter(guess: Double, x: Double): Double = {
  if (isGoodEnough(guess,x)) guess
  else sqrtIter(improve(guess,x),x)
}

def sqrt(x: Double) =
  sqrtIter(1, x)

sqrt(2)
```
