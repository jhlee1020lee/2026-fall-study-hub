---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 65
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Using a Wrapper Class
abstract class Iter[A] {
  def getValue: Option[A]
  def getNext: Iter[A]
}

class ListIter[A](val list: List[A]) extends Iter[A] {
  def getValue = list.headOption
  def getNext = new ListIter(list.tail)
}

sumElements((x:Int)=>x)(new ListIter(List(1,2,3,4)))
