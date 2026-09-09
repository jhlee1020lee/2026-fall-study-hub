---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 27
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Implement Iter and Listlike for List
// behaves like Listlike[A] <: Iter[A] in OOP
given listIter[L,A](using LL: Listlike[L,A]): Iter[L,A] with
  extension (l: L)
    def getValue = l.head
    def getNext = l.tail

// behaves like List[A] <: Listlike[A] in OOP
given listListlike[A]: Listlike[List[A],A] with
  extension (u: Unit)
    def unary_! = Nil
  extension (a: A)
    def ::(l: =>List[A]) = a::l
  extension (l: List[A])
    def head = l.headOption
    def tail = l.tail
    def ++(l2: List[A]) = l ::: l2
