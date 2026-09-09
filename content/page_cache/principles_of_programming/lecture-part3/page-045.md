---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 45
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Implementation using List
given BasicStack[A] : Stack[List[A],A] with
 extension (u: Unit)
   def empty = List()
 extension (s: List[A])
   def get = (s.head, s.tail)
   def put(a: A) = a :: s
