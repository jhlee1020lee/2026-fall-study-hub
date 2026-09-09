---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 40
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Lazy List
given lazylistListlike[A]: Listlike[LazyList[A],A] with
 extension (u: Unit)
   def unary_! = LNil
 extension (a: A)
   def ::(l: =>LazyList[A]) = LCons(a,l)
 extension (l: LazyList[A])
   def head = l.matches(None, (hd,tl) => Some(hd))
   def tail = l.matches(LNil, (hd,tl)=>tl)
   def ++(l2: LazyList[A]) = l.append(l2)


testList[LazyList[Int]]
testTree[MyTree[Int]]
testTree2[MyTree[Int]]
