---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Bag Example using type class
class Bag[A: Ord] protected (val toList: List[A])
{ def this() = this(Nil)
  def add(x: A) : Bag[A] = {
    def loop(elmts: List[A]) : List[A] =
     elmts match {
       case Nil => x :: Nil
       case e :: _ if (x < e) => x :: elmts
       case e :: _ if (x === e) => elmts
       case e :: rest => e :: loop(rest)
     }
    new Bag(loop(toList))
  }
}

(new Bag[Int]()).add(3).add(2).add(3).add(10).toList
