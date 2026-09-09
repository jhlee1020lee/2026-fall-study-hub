---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 63
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Lazy Iteration using LazyList
sealed abstract class MyTree[A] extends Iterable[A] {
  def iter : LazyList[A]
}
case class Empty[A]() extends MyTree[A] {
  val iter = LNil()
}                                    Note: “iter” is not recursive!!!
case class Node[A](value: A,
                    left: MyTree[A],
                    right: MyTree[A]) extends MyTree[A] {
  lazy val iter = LCons(value, left.iter.append(right.iter))
  // lazy val iter = left.iter.append(LCons(value,right.iter))
  // lazy val iter = left.iter.append(right.iter.append(
  //                    LCons(value,LNil())))
}
{ val t: MyTree[Int] = generateTree(200000)
  time (sumN((x:Int) => x)(100, t))
  time (sumN((x:Int) => x)(100000, t))
}
