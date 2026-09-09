---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 98
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Mixin Composition: A Better Way
trait MRIter[A] extends Iter[A] {
  def mapReduce[B,C](combine: (B,C)=>C, ival: C, f: A=>B): C = {
    def loop(c: Iter[A]): C = c.getValue match {
      case None => ival
      case Some(v) => combine(f(v), loop(c.getNext))
    }
    loop(this)
  }
}

class MRListIter[A](list: List[A])
  extends ListIter (list) with MRIter[A]

val mr = new MRListIter[Int](List(3,4,5))

// or, val mr = new ListIter(List(3,4,5)) with MRIter[Int]

mr.mapReduce[Int,Int]((b,c)=>b+c,0,(a)=>a*a)
