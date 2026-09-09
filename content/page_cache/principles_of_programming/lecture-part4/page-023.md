---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
String and str types

 fn main() {
   let mut s : &str = "abc";
   {
      let mut st : String = String::from(s);
      st.push_str("def"); // String::push_str(&mut st, "def");
      println!("{}", st);
      let s2 : &str = &st[1..4];
      // st.push_str("ghi");
      println!("{}", s2);
      // s = s2;
   }
   // println!("{}", s);
 }
