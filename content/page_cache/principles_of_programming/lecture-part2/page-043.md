---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Concrete Class: Implementation
// Written by Bob
sealed abstract class MyList[A] extends Iter[A]
case class MyNil[A]() extends MyList[A] {
   def getValue = None
   def getNext = throw new Exception("...")
}
case class MyCons[A](hd: A, tl: MyList[A])
   extends MyList[A]
{
   def getValue = Some(hd)
   def getNext = tl
}

val t1 = MyCons(3, MyCons(5, MyCons(7, MyNil())))

sumElementsId(t1)
