---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Sub Types for Records
• Example
  {val x: { val y: Int; val z: String}, val w: Int}
   <:        (by permutation)
  {val w: Int; val x: { val y: Int; val z: String}}
   <:        (by depth & width)
  {val w: Int; val x: {val z: String}}
