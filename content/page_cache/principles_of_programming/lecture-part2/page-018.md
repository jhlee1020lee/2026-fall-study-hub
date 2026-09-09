---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Class: No Structural Sub Typing
Ø Records: Structural sub-typing

                   foo_type <: gee_type

Ø Classes: Nominal sub-typing

                   gee_type <: foo_type

val v1 : gee_type = foo
val v2 : foo_type = gee // type error

def greeting(r:{val name:String}) =
  "Hi " + r.name + ", How are you?"
greeting(foo)
