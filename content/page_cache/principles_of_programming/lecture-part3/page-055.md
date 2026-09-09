---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 55
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Programs for Testing: use Iter, Iterable
def sumElements[I[_]](xs: I[Int])(implicit ITRA:Iterable[I]) = {
  def loop(i: ITRA.Itr[Int]): Int =
    i.getValue match {
      case None => 0
      case Some(n) => n + loop(i.getNext)
    }
  loop(xs.iter)
}

def printElements[I[_],A](xs: I[A])(implicit ITRA: Iterable[I]) = {
  def loop(i: ITRA.Itr[A]): Unit =
    i.getValue match {
      case None =>
      case Some(a) => {println(a); loop(i.getNext)}
    }
  loop(xs.iter)
}
