---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Bootstrapping Implicits
// lexicographic order
given tupOrd[A, B](using Ord[A], Ord[B]): Ord[(A,B)] with
 extension (self: (A,B))
   def cmp(a: (A, B)) : Int = {
     val c1 = self._1.cmp(a._1)
     if (c1 != 0) c1
     else { self._2.cmp(a._2) }
   }

val b = new Bag[(Int,(Int,Int))]
b.add((3,(3,4))).add((3,(2,7))).add((4,(0,0))).toList
