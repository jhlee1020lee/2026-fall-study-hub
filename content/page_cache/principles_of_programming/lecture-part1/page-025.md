---
title: "lecture-part1.pdf — page 25"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 25
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 25 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-024) · Page 25 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-026)

![lecture-part1.pdf — page 25](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-025.png)

## Extracted text

```text
Exercise: square root calculation
ØCalculate square roots with Newton’s method
def isGoodEnough(guess: Double, x: Double) =
  ??? // guess*guess is 99.9% close to x

def improve(guess: Double, x: Double) =
  (guess + x/guess) / 2

def sqrtIter(guess: Double, x: Double): Double =
  ??? // repeat improving guess until it is good enough

def sqrt(x: Double) =
  sqrtIter(1, x)

sqrt(2)
```
