---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Interfaces I: elimination
trait Iter[I,A]:
  extension (self: I)
   def getValue: Option[A]
   def getNext: I

trait Iterable[I,A]:
  type Itr
  given ITR: Iter[Itr,A]
  extension (self: I)
    def iter: Itr

// behaves like Iter[A] <: Iterable[A] in OOP
given iter2iterable[I,A](using _ITR: Iter[I,A]): Iterable[I,A] with
  type Itr = I
  def ITR = _ITR
  extension (self: I)
    def iter = self
