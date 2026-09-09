---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 106
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
IntStack: Core
ØCORE

class BasicIntStack protected (xs: List[Int]) extends Stack[Int]
{
  override val toString = "Stack:" + xs.toString
  def this() = this(Nil)

    def get():(Int,Stack[Int]) = (xs.head,new BasicIntStack(xs.tail))
    def put(x:Int): Stack[Int] = new BasicIntStack(x :: xs)
}

val s0 = new BasicIntStack
val s1 = s0.put(3)
val s2 = s1.put(-2)
val s3 = s2.put(4)
val (v1,s4) = s3.get()
val (v2,s5) = s4.get()
