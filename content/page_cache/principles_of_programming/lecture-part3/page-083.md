---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 83
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Heterogeneous List of Iter
trait Iter[I,A]:
  extension (i: I)
   def getValue: Option[A]
   def getNext: I

def sumElements[I](xs: I)(implicit ITR:Iter[I,Int]) : Int = {
  xs.getValue match {
    case None => 0
    case Some(n) => n + sumElements(xs.getNext)
  }
}

def sumElementsList(xs: List[dyn[curry1[Iter,Int]]]) : Int =
 xs match {
   case Nil => 0
   case hd :: tl => sumElements(hd.*) + sumElementsList(tl)
 }
