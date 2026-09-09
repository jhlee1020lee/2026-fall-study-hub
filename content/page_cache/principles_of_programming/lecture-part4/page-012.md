---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Values and Types

  A type defines a set of values.
  - For functionality, we only need to know the denotation of values.
  - For efficiency, we also need to know the shape of values.
  A value has a tree structure and consists of a header and bodies.
  - A header is data that may contain scalar values and pointers to bodies.
  - A body is data that must be stored in memory and may contain scalar
    values and pointers to other bodies.
  - When passing or storing a value, only its header is passed or stored.
  Types in Rust: i64, u64, (T1,T2), [T; 5], String, Vec<T>, …
                                             body
                                 body
                                             body
                 header
                                             body
                                 body
                                             body
