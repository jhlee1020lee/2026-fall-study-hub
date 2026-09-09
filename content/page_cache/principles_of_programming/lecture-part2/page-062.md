---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 62
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Solution 2: Lazy List
sealed abstract class LazyList[A] extends Iter[A] {
  def append(lst: LazyList[A]) : LazyList[A]
}

case class LNil[A]() extends LazyList[A] {
  def getValue = None
  def getNext = throw new Exception("")
  def append(lst: LazyList[A]) = lst
}

class LCons[A](hd: A, _tl: =>LazyList[A]) extends LazyList[A] {
  lazy val tl = _tl
  def getValue = Some(hd)
  def getNext = tl                    Note: “append” is not recursive!!!
  def append(lst: LazyList[A]) = LCons(hd, tl.append(lst)) }
object LCons {
  def apply[A](hd: A, tl: =>LazyList[A]) = new LCons(hd, tl)
}
