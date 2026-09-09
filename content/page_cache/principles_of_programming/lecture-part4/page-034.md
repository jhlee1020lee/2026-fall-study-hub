---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 34
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Recursive Enum with Box
 enum List<T> { Nil, Cons(T, Box<List<T>>) }
 impl <T> List<T> {
   fn new() -> List<T> { List::Nil }
   fn cons(hd: T, tl: List<T>) -> List<T> { List::Cons(hd, Box::new(tl)) }
 }
 fn mylen<T>(l: &List<T>) -> u64 {
   match l {
      List::Nil => 0,
      List::Cons(_, tl) => 1+mylen(tl) // 1+mylen(tl.as_ref())
   }
 }
 fn main() {
   let l = List::cons(0, List::cons(1, List::cons(2, List::new())));
   println!("{}", mylen(&l));
 }
