---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 94
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Test
def sumElements[A](f: A=>Int)(xs: Iter[A]) : Int =
  xs.getValue match {
    case None => 0
    case Some(n) => f(n) + sumElements(f)(xs.getNext)
  }

def find3(d: Dict[Int,String]) = {
  d.find(3)
}

val d0 = new ListIterDict[Int,String]((x,y)=>x==y,Nil)
val d = d0.add(4,"four").add(3,"three")

sumElements[(Int,String)](x=>x._1)(d)
find3(d)
