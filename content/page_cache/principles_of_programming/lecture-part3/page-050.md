---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 50
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Implementation: Sorted Stack
def SortedStack : Stack[List[Int],Int] = new {
 extension (u: Unit)
   def empty = List()
 extension (s: List[Int])
   def get = (s.head, s.tail)
   def put(a: Int) : List[Int] = {
     def loop(l: List[Int]) : List[Int] = l match {
       case Nil => a :: Nil
       case hd :: tl => if (a <= hd) a :: l else hd :: loop(tl)
     }
     loop(s)
   }
 }

testStack(Filtering(Incrementing(Doubling(SortedStack))))
