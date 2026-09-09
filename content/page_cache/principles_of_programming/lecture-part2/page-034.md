---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 34
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Case Class
sealed abstract class MyList[A] { … }
case class MyNil[A]() extends MyList[A] { … }
object MyNil { def apply[A]() = new MyNil[A]() }
case class MyCons[A](val hd: A, val tl: MyList[A])
  extends MyList[A] { … }
object MyCons {
  def apply[A](hd:A, tl:MyList[A]) = new MyCons[A](hd, tl)}
val t: MyList[Int] = MyCons(3, MyNil())
             Allow Pattern Matching
def length(x: MyList[Int]): Int =
  x match {
     case MyNil() => 0
     case MyCons(hd, tl) => 1 + length(tl)
  }
Cf. sealed abstract class MyList[A]
