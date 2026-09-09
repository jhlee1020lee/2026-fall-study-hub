---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 51
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Closure construction: move
 fn test1<F>(f: F) -> usize
 where F: Fn(usize)->usize {
   f(10) + f(20)
 }
 fn main() {
   let clo;
   {
      let s = "abc".to_string();
      clo = move|n|n+s.len();
   }
   println!("{}", test1(clo));
 }
