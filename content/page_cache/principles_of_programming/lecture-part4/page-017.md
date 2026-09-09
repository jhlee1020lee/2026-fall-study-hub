---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 17
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Principles of Ownership

 <Ownership rules>
 - A header must be stored in exactly one location, which owns the header.
 - Every heap block must be owned by exactly one header that directly
   points to it.
 - Headers can be moved between locations.
 - Headers are dropped when their owner is freed or overwritten.
 - When dropped, a header's owned heap blocks are also freed.
 - A stack variable is freed when it goes out of scope.

 <Borrowing rules> (known as, “mutation-xor-sharing” checking)
 - Mutable: single borrower has exclusive read/write access.
 - Immutable: multiple borrowers and owner can read.
