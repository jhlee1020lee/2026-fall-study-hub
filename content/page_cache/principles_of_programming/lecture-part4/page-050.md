---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 50
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Closure type: FnOnce
 fn test3<F>(f: F)->String
 where F: FnOnce(&str)->String {
   f("test")
 }
 fn main() {
   let mut s = "abc".to_string();
   let f1 = |n|n+s.len();
   println!("{}", test1(f1));
   let f2 = |x:&str|s.push_str(x);
   test2(f2);
   println!("{}", s);
   let f3 = move|x:&str|{s.push_str(x); s}; // can omit "move"
   let s2 = test3(f3);
   println!("{}", s2);
 }
