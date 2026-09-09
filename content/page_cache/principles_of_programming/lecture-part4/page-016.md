---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Issues with mutation and deallocation for memory

 <Problematic mutations>
 Multiple parties modify a value logically simultaneously.
 - Problem
   The value may become inconsistent despite valid individual updates.

 A value is read logically simultaneously while being modified.
 - Problem
   An inconsistent intermediate state may be read.

 <Problematic deallocation>
 A value’s body is deallocated while its header remains accessible.
 - Problem
   The deallocated body may be accessed via the header (use-after-free
   bug).
