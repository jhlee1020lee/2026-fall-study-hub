---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Interfaces II: introduction + elimination
trait Listlike[L,A]:
  extension(u:Unit)
   def unary_! : L
  extension(elem:A)
   def ::(l: =>L): L
  extension(l: L)
   def head: Option[A]
   def tail: L
   def ++(l2: L): L
trait Treelike[T,A]:
  extension(u:Unit)
   def unary_! : T
  extension(a:A)
   def has(lt: T, rt: T): T
  extension(t: T)
   def root : Option[A]
   def left : T
   def right : T
