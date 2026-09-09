---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 68
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
List with Map
trait Maplike[L[_]]:
  extension[A](l: L[A])
   def map[B](f: A => B): L[B]

def testMapList[L[_]](implicit LL: Listlike[L], ML: Maplike[L], ITR: Iter[L]) = {
  val l1 = 3.3 :: 2.2 :: 1.5 :: !()
  val l2 = l1.map((n:Double)=>n.toInt)
  val l3 = l2.map((n:Int)=>n.toString)
  printElements(l3)
}
