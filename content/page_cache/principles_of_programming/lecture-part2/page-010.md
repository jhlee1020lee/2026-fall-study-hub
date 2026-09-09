---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Sub Types for Special Types
• Nothing: The empty set
• Any: The set of all values

• For any type T, we have:
                       Nothing <: T <: Any

• Example
  val a : Int = 3
  val b : Any = a
  def f(a: Nothing) : Int = a
