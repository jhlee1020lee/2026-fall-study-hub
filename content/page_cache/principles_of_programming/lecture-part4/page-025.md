---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Function Types with lifetime annotation

 fn foo<'a> (s: &'a mut String) -> &'a str { return &s[0..2]; }
 fn gee(f: for <'a> fn(&'a mut String) -> &'a str) {
   let s;
   {
      let mut a = String::from("test");
      let s1 = f(&mut a); // &mut a is assumed to be expired within f
      let s2 = s1; // let s2 = &a
      println!("{} {}", s1, s2); // s1, s2 are droped here since no longer used
      a.push_str("123"); println!("{}", a);
      s = f(&mut a); println!("{}", s);
   } // s is droped here because a is freed here
   // println!("{}", s);
 }
 fn main() { gee(foo); }
