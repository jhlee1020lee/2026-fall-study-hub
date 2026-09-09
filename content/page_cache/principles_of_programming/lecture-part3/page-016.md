---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
With Different Orders
def intOrdRev : Ord[Int] = new {
  extension (self: Int)
   def cmp(a: Int) = a - self
}

(new Bag[Int]()).add(3).add(2).add(10).toList
(new Bag[Int]()(intOrdRev)).add(3).add(2).add(10).toList
