---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Simplification using Argument Members
class MyList[A](v: A, nxt: Option[MyList[A]]) {
  val value : A = v
  val next : Option[MyList[A]] = nxt
}


class MyList[A](val value:A, val next:Option[MyList[A]]) {
}


class MyList[A](val value:A, val next:Option[MyList[A]])
