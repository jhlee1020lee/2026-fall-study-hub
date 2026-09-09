---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 35
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Exercise
Define “MyTree[A]” using sub class.

class MyTree[A](v: A,
                 lt: Option[MyTree[A]],
                 rt: Option[MyTree[A]]) {
  val value = v
  val left = lt
  val right = rt
}

type YourTree[A] = Option[MyTree[A]]
