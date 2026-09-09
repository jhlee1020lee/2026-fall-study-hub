---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 77
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
MyTree
sealed abstract class MyTree[A] extends IterableHE[A] {
  type iter_t = List[A]
  def getValue(i : List[A]) : Option[A] = i.headOption
  def getNext(i: List[A]) : List[A] = i.tail
}
case class Empty[A](_eq:(A,A)=>Boolean) extends MyTree[A] {
  def eq(a:A, b:A) = _eq(a,b)
  val iter : List[A] = Nil
}
case class Node[A](_eq: (A,A)=>Boolean,
               value: A, left: MyTree[A], right: MyTree[A])
  extends MyTree[A] {
  def eq(a:A, b:A) = _eq(a,b)
  val iter : List[A] = value :: (left.iter ++ right.iter)
}
