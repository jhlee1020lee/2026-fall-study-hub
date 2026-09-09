---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Scalar Types

 fn main() {
   let mut x = [1,2,3,4];
   println!("{}", x[2]);
   x[2] = 42;
   println!("{}", x[2]);
   let y = x;
   println!("{}", x[0]);
   println!("{}", y[0]);
 }
