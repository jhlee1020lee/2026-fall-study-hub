---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Sub Types
• The sub type relation is kind of the subset relation.
• But they are NOT the same.

• T <: S
  Every element of T can be used as that of S.

• Cf. T is a subset of S.
  Every element of T is that of S.

• Why polymorphism?
  A function of type S=>R can be used as T=>R for many sub
  types T of S.
  Note that S=>R <: T=>R when T <: S.
