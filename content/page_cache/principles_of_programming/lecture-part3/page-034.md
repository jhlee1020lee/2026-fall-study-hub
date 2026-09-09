---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 34
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Test for Lazy List
def time[R](block: => R): R = {
  val t0 = System.nanoTime()
  val result = block // call-by-name
  val t1 = System.nanoTime()
  println("Elapsed time: " + ((t1 - t0)/1000000) + "ms"); result
}
def sumN[I](n: Int, t: I)(implicit ITRA: Iterable[I,Int]): Int = {
  def go(res: Int, n: Int, itr: ITRA.Itr): Int =
   if (n <= 0) res
   else itr.getValue match {
     case None => res
     case Some(v) => go(v + res, n - 1, itr.getNext)
   }
  go(0, n, t.iter)
}
