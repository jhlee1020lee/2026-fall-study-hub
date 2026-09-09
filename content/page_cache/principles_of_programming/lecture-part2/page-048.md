---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 48
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Problem: Iter for MyTree
abstract class Iter[A] {
  def getValue: Option[A]
  def getNext: Iter[A]
}

// Written by David
sealed abstract class MyTree[A]
case class Empty[A]() extends MyTree[A]
case class Node[A](value: A,
                    left: MyTree[A],
                    right: MyTree[A]) extends MyTree[A]

Q: Can MyTree[A] implement Iter[A]?
   Try it, but it is not easy.
