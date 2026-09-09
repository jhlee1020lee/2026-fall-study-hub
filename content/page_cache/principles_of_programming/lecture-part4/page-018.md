---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Principles of Lifetime

 <Lifetime definition>
 - Stack variables have a static lifetime bound by their scope.
 - Heap blocks have a dynamic lifetime that ends when their owner is
   dropped.
 - Headers have a dynamic lifetime that ends when their owner is freed or
   overwritten.

 <Lifetime rules for borrowing> (known as, “borrow lifetime checking”)
 - A location's lifetime must be longer than any of its borrowers' lifetimes.
