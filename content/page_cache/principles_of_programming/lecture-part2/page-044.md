---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 44
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Exercise
Define IntCounter(n) that implements the interface Iter[A].

// Written by Catherine
class IntCounter(n: Int) extends Iter[Int] {
   def getValue = ???
   def getNext = ???
}

sumElementsId(new IntCounter(100))
