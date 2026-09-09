---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 78
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Test
val Ieq = (x:Int,y:Int) => x == y
val IEmpty = Empty(Ieq)
def INode(n: Int, t1: MyTree[Int], t2: MyTree[Int]) =
  Node(Ieq,n,t1,t2)

val t : MyTree[Int] =
  INode(3, INode(4,INode(2,IEmpty,IEmpty),
                   INode(3,IEmpty,IEmpty)),
           INode(5,IEmpty,IEmpty))

sumElements((x:Int)=>x)(t)
t.hasElement(5)
t.hasElement(10)
