---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 91
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Motivation
abstract class Iter[A] {
  def getValue: Option[A]
  def getNext: Iter[A]
}

class ListIter[A](val list: List[A]) extends Iter[A] {
  def getValue = list.headOption
  def getNext = new ListIter(list.tail)
}

abstract class Dict[K,V] {
  def add(k: K, v: V): Dict[K,V]
  def find(k: K): Option[V]
}

Q: How can we extend ListIter and implement Dict?
