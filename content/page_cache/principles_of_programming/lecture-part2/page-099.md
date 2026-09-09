---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 99
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Syntactic Sugar: new A with B with C { … }
new A(...) with B1 … with Bm {
  code
}

is equivalent to

{
    class _tmp_(args) extends A(args) with B1 … with Bm {
      code
    }
    new _tmp_(...)
}
