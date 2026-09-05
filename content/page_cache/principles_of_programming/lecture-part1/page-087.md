---
title: "lecture-part1.pdf — page 87"
course: "principles_of_programming"
source_pdf: "lecture-part1.pdf"
pdf_page: 87
source_url: "https://github.com/snu-sf-class/pp202602"
source_url_kind: "course_repository"
source_pdf_public: false
publication_mode: "preview_only"
generated_at: "2026-09-05T08:10:11Z"
---

**Source:** `lecture-part1.pdf` · page 87 of 100.

[Course source repository (not a direct PDF link)](https://github.com/snu-sf-class/pp202602). Only page previews are hosted here; the original PDF is not mirrored.

[Previous page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-086) · Page 87 / 100 · [Next page](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/principles_of_programming/lecture-part1/page-088)

![lecture-part1.pdf — page 87](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/principles_of_programming/lecture-part1/page-087.png)

## Extracted text

```text
What Are Types For?
Ø Typed Programming
  def id1(x: Int): Int = x
  def id2(x: Double): Double = x
  • At run time, type information is erased (ie, id1 = id2)
Ø Untyped Programming
  def id(x) = x
  • Do not care about types at compile time.
  • But, many such languages check types at run time paying cost.
  • Without run-time type check, errors can be badly propagated.
Ø What is compile-time type checking for?
  • Can detect type errors at compile time.
  • Increase Readability (Give a good abstraction).
  • Soundness: Well-typed programs raise no type errors at run time.
```
