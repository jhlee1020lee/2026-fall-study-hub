---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 69
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Using an Associate Type
abstract class Iterable[A] {
  type iter_t
  def iter: iter_t
  def getValue(i: iter_t) : Option[A]
  def getNext(i: iter_t) : iter_t
}

def sumElements[A](f:A=>Int)(xs: Iterable[A]) : Int = {
  def sumElementsIter(i: xs.iter_t) : Int =
    xs.getValue(i) match {
      case None => 0
      case Some(n) => f(n) + sumElementsIter(xs.getNext(i))
    }
  sumElementsIter(xs.iter)
}
