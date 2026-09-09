---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Solution
class MyTree[A](v: A,
                 lt: Option[MyTree[A]],
                 rt: Option[MyTree[A]]) {
  val value = v
  val left = lt
  val right = rt
}

type YourTree[A] = Option[MyTree[A]]

val t0 : YourTree[Int] = None
val t1 : YourTree[Int] = Some(new MyTree(3, None, None))
val t2 : YourTree[Int] =
  Some(new MyTree(3, Some (new MyTree(4,None,None)), None))
