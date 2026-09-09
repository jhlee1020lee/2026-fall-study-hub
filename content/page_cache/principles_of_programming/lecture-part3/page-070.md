---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 70
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
List with Map
given listMaplike: Maplike[List] with
extension [A](l: List[A])
   def map[B](f: A => B) = l.map(f)

testMapList[List]
