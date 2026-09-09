---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 40
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Rc type
 Use Rc type to replace static lifetime checking with dynamic checking.

 <Problem>
 enum List<T> {
   Cons(T, Rc<List<T>>),
   Nil,
 }
 use crate::List::*;
 fn test() -> (List<i64>,List<i64>) {
   let a = Cons(5, Box::new(Nil));
   let b = Cons(3, Box::new(a));
   let c = Cons(4, Box::new(a));
   (b,c)
 }
