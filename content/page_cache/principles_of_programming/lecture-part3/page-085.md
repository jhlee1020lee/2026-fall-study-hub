---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 85
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Test
given listIter[A]: Iter[List[A],A] with
 extension (l: List[A])
   def getValue = l.headOption
   def getNext = l.tail

given decIter : Iter[Int,Int] with
 extension (i: Int)
   def getValue = if (i >= 0) Some(i) else None
   def getNext = i - 1

sumElementsList(List(
 100,
 List(1,2,3),
 10))
