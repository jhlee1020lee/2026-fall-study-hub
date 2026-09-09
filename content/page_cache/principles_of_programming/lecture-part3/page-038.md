---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 38
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Lazy List
sealed abstract class LazyList[+A] {
  def matches[R](caseNil: =>R, caseCons: (A,LazyList[A])=>R) : R
}
case object LNil extends LazyList[Nothing] {
  def matches[R](caseNil: =>R, _u: (Nothing,LazyList[Nothing])=>R) =
    caseNil
}
class LCons[A](hd: A, _tl: =>LazyList[A]) extends LazyList[A] {
  lazy val tl = _tl
  def matches[R](_u: =>R, caseCons: (A, LazyList[A])=>R) =
    caseCons(hd, tl)
}
object LazyList {
  extension [A](l: LazyList[A])
    def append(l2: LazyList[A]) : LazyList[A] =
     l.matches(l2, (hd,tl) => LCons(hd, tl.append(l2)))
}
import LazyList.*
