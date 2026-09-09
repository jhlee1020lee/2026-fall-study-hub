---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 61
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Lazy Iteration using Lists of Trees
sealed abstract class MyTree[A] extends Iterable[A]
case class Empty[A]() extends MyTree[A] {
  val iter = new MyTreeIter(MyNil())
}
case class Node[A](value: A,
                   left: MyTree[A],
                   right: MyTree[A]) extends MyTree[A]
{
  val iter = new MyTreeIter(MyCons(this,MyNil()))
}

{ val t: MyTree[Int] = generateTree(200000)
  time (sumN((x:Int) => x)(100, t))
  time (sumN((x:Int) => x)(100000, t))
}
