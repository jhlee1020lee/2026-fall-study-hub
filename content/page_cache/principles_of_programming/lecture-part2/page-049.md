---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 49
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Possible Solution
// Written by David
sealed abstract class MyTree[A] extends Iter[A]
case class Empty[A]() extends MyTree[A] {
  def getValue = None
  def getNext = this }
case class Node[A](value: A, left: MyTree[A], right: MyTree[A])
     extends MyTree[A] {
  def getValue = Some(value)
  def getNext: MyTree[A] = {
   def merge_right(l : MyTree[A]): MyTree[A] = l match {
    case Empty() => right
    case Node(v, lt, rt) => Node(v, lt, merge_right(rt)) }
   merge_right(left) } }
val t1 = Node(3, Node(7, Node(2, Empty(), Empty()), Empty()),
               Node(8, Empty(), Empty()))
sumElements[Int]((x)=>x*x)(t1)
