---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 61
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
List: provide Iter, ListIF
// behaves like List[A] <: Iter[A] in OOP
given listIter: Iter[List] with
  extension [A](l: List[A])
    def getValue = l.headOption
    def getNext = l.tail

// behaves like List[A] <: Listlike[A] in OOP
given listListlike: Listlike[List] with
  extension [A](u: Unit)
    def unary_! = Nil
  extension [A](a: A)
    def ::(l: =>List[A]) = a::l
  extension [A](l: List[A])
    def head = l.headOption
    def tail = l.tail
    def ++(l2: List[A]) = l ::: l2
