---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 20
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Rust’s approach

 - References to a location of type T:
    - &T: immutable reference
    - &mut T: mutable reference

 - Function signatures specify ownership/lifetime conditions

 - Compiler checks ownership/lifetime in Safe Rust at two levels:
    - Stack variables (assuming used functions’ signatures)
    - A function’s argument and return value (verifying against its signature)

 - Heap Memory Management:
    - Experts implement primitive heap types in Unsafe Rust with
      ownership/lifetime guarantees specified in function signatures
    - Users compose these primitives in Safe Rust to build complex data
      structures
