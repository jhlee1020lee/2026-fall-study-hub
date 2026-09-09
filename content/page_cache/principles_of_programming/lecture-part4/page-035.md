---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 35
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Update via a mutable reference
 use std::mem;
 fn test(x: &mut List<i32>) {
   // *x = List::cons(0, *x)
   let old = mem::replace(x, List::new());
   *x = List::cons(0, old)
 }

 fn main() {
   let mut l = List::cons(0, List::cons(1, List::cons(2, List::new())));
   println!("{}", mylen(&l));
   test(&mut l);
   println!("{}", mylen(&l));
 }
