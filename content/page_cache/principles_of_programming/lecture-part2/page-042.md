---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 42
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Abstract Class: Interface
ØExample Interface
// Written by Alice
// if getValue(i) returns None, you should not use i.getNext()
abstract class Iter[A] {
    def getValue: Option[A]
    def getNext: Iter[A]
}

def sumElements[A](f: A=>Int)(xs: Iter[A]) : Int =
  xs.getValue match {
    case None => 0
    case Some(n) => f(n) + sumElements(f)(xs.getNext)
  }
def sumElementsId(xs:Iter[Int]) =
  sumElements((x:Int)=>x)(xs)
