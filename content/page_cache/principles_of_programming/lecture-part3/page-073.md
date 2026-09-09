---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 73
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Interfaces
trait DataProcessor[D]:
  extension (d: D)
   def input(s: String) : D
   def output : String

trait DPFactory:
  extension (u: Unit)
   def getTypes: List[String]
   def makeDP(dptype: String) : ???

def run(implicit factory: DPFactory) : Unit


How to return data with associated functions like OOP?
