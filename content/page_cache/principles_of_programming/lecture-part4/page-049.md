---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 49
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Closure type: FnMut
 fn test2<F>(mut f: F)
 where F: FnMut(&str)->() {
   f("gil");
   f("hur");
 }
 fn main() {
   let mut s = "abc".to_string();
   let f1 = |n|n+s.len();
   println!("{}", test1(f1));
   let f2 = |x:&str|s.push_str(x);
   test2(f2);
   println!("{}", s);
 }
