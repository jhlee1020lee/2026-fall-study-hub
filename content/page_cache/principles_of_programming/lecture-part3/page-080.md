---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 80
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Data Processor
given dpfactory: DPFactory with
 extension (u: Unit)
   def getTypes = List("sum", "mult")
   def makeDP(dptype: String) = {
     if (dptype == "sum")
       makeProc(0, (x, y) => x + y)
     else
       makeProc(1, (x, y) => x * y)
   }

  def makeProc(init: Int, op: (Int, Int) => Int): dyn[DataProcessor] = {
    given dp: DataProcessor[Int] with
      extension (d: Int)
       def input(s: String) = op(d, s.toInt)
       def output = d.toString()
    init     // dyn(init) // dyn.apply[Int,DataProcessor](init)(dp)
  }
