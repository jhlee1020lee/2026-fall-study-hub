---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 44
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
RefCell type
 fn test() -> (List<i64>,List<i64>) {
   let a = Rc::new(RefCell::new(Cons(5, Rc::new(RefCell::new(Nil)))));
   let b = Cons(3, Rc::clone(&a));
   let c = Cons(4, Rc::clone(&a));
   (b,c)
 }
 fn main() {
   let (mut l1, l2) = test();
   {
      let mut r = l1.unfold_mut().unwrap().1;
      *r = Cons(42, Rc::new(RefCell::new(Nil)));
   }
   println!("{}", l2.unfold().unwrap().1.unfold().unwrap().0)
 }
