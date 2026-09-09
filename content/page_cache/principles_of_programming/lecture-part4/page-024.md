---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 24
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Borrow and re-borrow

 // We track borrow & re-borrow relations
 fn main() {
    let mut st : String = String::from("abc");
    {
       let stp1 : &mut String = &mut st; // borrow
       {
          let stp2 : &mut String = stp1; // re-borrow
          // stp1.push_str("def");
          stp2.push_str("def");
       }
       stp1.push_str("ghi");
    }
    println!("{}", st);
 }
