---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Types with Ownership

➢ Ownership Types

  • expresses and guarantees immutability
   - making code behavior more predictable

  • automatically deallocates memory when its ownership has gone
   - guaranteeing absence of use-after-free, double-free, memory-leak

  • disallows mutating the same value at the same time
   - guaranteeing data-race freedom in concurrent code


      Programming with Mutation in a Principled Way!
