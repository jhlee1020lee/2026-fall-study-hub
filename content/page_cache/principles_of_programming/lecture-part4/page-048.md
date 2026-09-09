---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 48
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Closure type: Fn
 fn test1<F>(f: F) -> usize
 where F: Fn(usize)->usize {
   f(10) + f(20)
 }
 fn main() {
   let mut s = "abc".to_string();
   let f1 = |n|n+s.len();
   println!("{}", test1(f1));
 }
