---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 78
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Test
def test(implicit DF: DPFactory) = {
  def go(types: List[String]) : Unit =
   types match {
     case Nil => ()
     case ty :: rest => {
       val dp = ().makeDP(ty)
       println(dp.*.input("10").input("20").output)
       go(rest)
     }
   }
  val types = ().getTypes
  println(types)
  go(types)
}
