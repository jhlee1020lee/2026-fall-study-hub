---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
RefCell type
 use std::rc::Rc; use std::cell::{RefCell, Ref, RefMut};
 enum List<T> {
    Cons(T, Rc<RefCell<List<T>>>),
    Nil,
 }
 use crate::List::{Cons, Nil};
 impl <T> List<T> {
    fn unfold<'a>(&'a self) -> Option<(&'a T, Ref<'a, List<T>>)> {
       if let Cons(hd,tl) = self { Some((hd, tl.borrow())) } else { None }
                                          // tl.as_ref().borrow()
    }
    fn unfold_mut<'a>(&'a mut self) -> Option<(&'a mut T, RefMut<'a,
 List<T>>)> {
       if let Cons(hd,tl) = self { Some((hd,tl.borrow_mut())) } else { None }
    }}
