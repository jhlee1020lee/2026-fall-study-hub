---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 73
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Abstract Class with Arguments
abstract class IterableH[A] extends Iterable[A] {
  def hasElement(a: A) : Boolean
}
abstract class IterableHE[A](eq: (A,A) => Boolean)
   extends IterableH[A]
{
   def hasElement(a: A) : Boolean = {
     def hasElementIter(i: iter_t) : Boolean =
       getValue(i) match {
         case None => false
         case Some(n) =>
            if (eq(a,n)) true
            else hasElementIter(getNext(i))
       }
     hasElementIter(iter)
   }
