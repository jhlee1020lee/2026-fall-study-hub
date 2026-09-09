---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Example: MyList with match
abstract class MyList[A]() {
  def matches[R](nilE: =>R, consE: (A,MyList[A]) => R) : R
}
class MyNil[A]() extends MyList[A] {
  def matches[R](nilE: =>R, consE: (A,MyList[A]) => R) : R =
    nilE
}
class MyCons[A](val hd: A, val tl: MyList[A]) extends MyList[A] {
  def matches[R](nilE: =>R, consE: (A,MyList[A]) => R) : R =
    consE(hd,tl)
}
def length[A](l: MyList[A]) : Int =
  l.matches(0,
            (hd, tl) => 1 + length(tl))

length(new MyCons(10, new MyCons(5, new MyNil())))
