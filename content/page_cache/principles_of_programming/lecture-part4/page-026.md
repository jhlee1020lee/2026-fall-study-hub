---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 26
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Lifetime Elision Rules
 Elision rules are as follows:
 • Each elided lifetime in input position becomes a distinct lifetime parameter.
 • If there is exactly one input lifetime position (elided or not), that lifetime is
   assigned to allelided output lifetimes.
 • If there are multiple input lifetime positions, but one of them is &self or
   &mut self, the lifetime of self is assigned to all elided output lifetimes.

 fn foo(s: &mut String) -> &str { return &s[0..2]; }
 fn gee(f: fn(&mut String) -> &str) {
   ...
 }
 fn main() { gee(foo); }
