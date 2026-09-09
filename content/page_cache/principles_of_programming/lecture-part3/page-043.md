---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
IntStack Spec
trait Stack[S,A]:
  extension (u: Unit)
   def empty : S
  extension (s: S)
   def get: (A,S)
   def put(a: A): S

def testStack[S](implicit STK: Stack[S,Int]) = {
  val s = ().empty.put(3).put(-2).put(4)
  val (v1,s1) = s.get
  val (v2,s2) = s1.get
  (v1,v2)
}
