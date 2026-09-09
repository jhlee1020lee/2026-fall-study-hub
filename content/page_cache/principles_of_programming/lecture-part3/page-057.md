---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 57
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Interfaces II
trait Listlike[L[_]]:
  extension[A](u:Unit)
   def unary_! : L[A]
  extension[A](elem:A)
   def ::(l: =>L[A]): L[A]
  extension[A](l: L[A])
   def head: Option[A]
   def tail: L[A]
   def ++(l2: L[A]): L[A]
trait Treelike[T[_]]:
  extension[A](u:Unit)
   def unary_! : T[A]
  extension[A](a:A)
   def has(lt: T[A], rt: T[A]): T[A]
  extension[A](t: T[A])
   def root : Option[A]
   def left : T[A]
   def right : T[A]
