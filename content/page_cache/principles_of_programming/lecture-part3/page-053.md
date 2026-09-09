---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 53
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Interfaces I
// eg. Iter[List]
trait Iter[I[_]]:                          // trait Iter[I,A]:
  extension [A](i: I[A])                   // extension (i: I)
    def getValue: Option[A]                // def getValue: Option[A]
    def getNext: I[A]                      // def getNext: I

// eg. Iterable[MyTree]
trait Iterable[I[_]]:                      // trait Iterable[I,A]:
  type Itr[_]                              // type Itr
  given ITR: Iter[Itr]                     // given ItrI: Iter[Itr,A]
  extension [A](i: I[A])                   // extension (i: I)
    def iter: Itr[A]                       // def iter: Itr

given iter2iterable[I[_]](using _ITR: Iter[I]): Iterable[I] with
 type Itr[A] = I[A]
 def ITR = _ITR
 extension [A](i:I[A])
   def iter = i
