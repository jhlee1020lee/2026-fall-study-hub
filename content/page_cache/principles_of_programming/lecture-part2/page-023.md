---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Simplification using Companion Object
class MyList[A](val value:A, val next:Option[MyList[A]])
object MyList
{ def apply[A](v: A, nxt: Option[MyList[A]]) =
    new MyList(v,nxt)
}

type YourList[A] = Option[MyList[A]]
object YourList
{ def apply[A](v: A, nxt: Option[MyList[A]]) =
    Some(new MyList(v,nxt))
}
val t0 = None
val t1 = Some(new MyList(3,Some(MyList(4,None))))
val t2 = YourList(3,(YourList(4,None)))
