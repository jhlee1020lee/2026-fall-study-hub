---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 26
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Simplified Solution

class MyTree[A](val value : A,
                val left : Option[MyTree[A]],
                val right : Option[MyTree[A]])

type YourTree[A] = Option[MyTree[A]]

object YourTree
{ def apply[A](v:A, lt:Option[MyTree[A]], rt:Option[MyTree[A]]) =
    Some(new MyTree(v,lt,rt))
}

val t0: YourTree[Int] = None
val t1: YourTree[Int] = YourTree(3,None,None)
val t2: YourTree[Int] = YourTree(3,YourTree(4,None,None),None)
