---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Heap memory with dynamic size and dynamic lifetime

  Heap memory consists of blocks of all types (ie, dynamic sizes) with
  no scopes (ie, dynamic lifetime).
  A heap block can be a body of a value, which can also store headers of
  other values.

  // variable sz of type usize (8-byte header) with Scope 1
  fn gee(sz: usize) -> Vec<i64> {
  // variable v of type Vec<i64> (24-byte header) with Scope 1
  // The header points to a heap block of (sz * 8) bytes, filled with zeros
     let v : Vec<i64> = vec![0; sz];
  // The header goes out of Scope 1 and the heap block is still alive
     return v;
  } // Scope 1
