---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 39
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Encoding ADT using classes: Monotonicity
sealed abstract class MyList[+A] {
  def matches[R](nilE: =>R, consE: (A,MyList[A])=>R) : R
  def append[B>:A](l: MyList[B]) : MyList[B]
}
object MyNil extends MyList[Nothing] {
  def matches[R](nilE: =>R, consE: (Nothing,MyList[Nothing])=>R) = nilE
  def append[B](l: MyList[B]) = l
}
class MyCons[A](val hd: A, val tl: MyList[A]) extends MyList[A] {
  def matches[R](nilE: =>R, consE: (A,MyList[A])=>R) = consE(hd,tl)
  def append[B>:A](l: MyList[B]) = new MyCons[B](hd, tl.append(l))
}
object MyCons{ def apply[A](hd:A, tl:MyList[A]) = new MyCons[A](hd, tl) }
def length[A](l: MyList[A]) : Int =
  l.matches(
    0,
    (_,tl) => 1 + length(tl) )
length(MyCons(3, MyCons(2, MyNil)).append(MyCons(1,MyNil)))
