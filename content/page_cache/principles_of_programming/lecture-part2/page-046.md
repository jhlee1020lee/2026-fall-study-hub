---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 46
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
A Better Interface
abstract class Iter[A] {
  def get: Option[(A,Iter[A])]
}
def sumElements[A](f: A=>Int)(xs: Iter[A]) : Int =
  xs.get match {
    case None => 0
    case Some(n,nxt) => f(n) + sumElements(f)(nxt)
  }
def sumElementsId(xs:Iter[Int]) = sumElements((x:Int)=>x)(xs)
sealed abstract class MyList[A] extends Iter[A]
case class MyNil[A]() extends MyList[A] {
  def get = None }
case class MyCons[A](hd: A, tl: MyList[A]) extends MyList[A] {
  def get = Some(hd,tl) }
class IntCounter(n: Int) extends Iter[Int] {
  def get = if (n >= 0) Some(n, new IntCounter(n-1)) else None }
