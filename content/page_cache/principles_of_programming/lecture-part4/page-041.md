---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 41
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Rc type
 use std::rc::Rc;
 enum List<T> { Cons(T, Rc<List<T>>), Nil, }
 use crate::List::*;
 impl <T> List<T> {
   fn unfold(&self) -> Option<(&T,&List<T>)> {
      if let Cons(hd,tl) = self { Some((hd, tl.as_ref())) } else { None }
   }}
 fn test() -> (List<i64>,List<i64>) {
   let a = Rc::new(Cons(5, Rc::new(Nil)));
   let b = Cons(3, Rc::clone(&a));
   let c = Cons(4, Rc::clone(&a));
   (b,c) }
 fn main() {
   let (l1, l2) = test(); { let _t = l1; }
   println!("{}", l2.unfold().unwrap().1.unfold().unwrap().0) }
