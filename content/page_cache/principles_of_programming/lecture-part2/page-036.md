---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 36
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Solution
sealed abstract class MyTree[A]
case class Empty[A]() extends MyTree[A]
case class Node[A](value:A, left:MyTree[A], right:MyTree[A])
  extends MyTree[A]

val t : MyTree[Int] =
  Node(3, Node(4,Empty(),Empty()), Empty())

t match {
  case Empty() => 0
  case Node(v,l,r) => v
}
