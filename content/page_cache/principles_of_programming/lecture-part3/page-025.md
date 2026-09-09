---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Programs for Testing: use All
def testList[L](implicit LL: Listlike[L,Int], ITRA: Iterable[L,Int]) = {
  val l = (3 :: !()) ++ (1 :: 2 :: !())
  println(sumElements(l))
  printElements(l)
}

def testTree[T](implicit TL: Treelike[T,Int], ITRA: Iterable[T,Int]) = {
  val t = 3.has(4.has(!(), !()), 2.has(!(),!()))
  println(sumElements(t))
  printElements(t)
}
