---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 36
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Test for Lazy List
def testTree2[T](implicit TL: Treelike[T,Int], ITRA: Iterable[T,Int]) = {
 def generateTree(n: Int): T = {
   def gen(lo: Int, hi: Int): T = {
     if (lo > hi) !()
     else {
       val mid = (lo + hi) / 2
       mid.has(gen(lo, mid - 1), gen(mid + 1, hi))
     }
   }
   gen(1, n)
 }

    // Problem: takes a few seconds to get a single value
    { val t = generateTree(200000)
      time (sumN(2, t)) }
}
