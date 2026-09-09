---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Enum
 enum IpAddr {
   V4(u8, u8, u8, u8),
   V6(String),
 }
 use IpAddr::*;
 fn main() {
   let ip1 : IpAddr = V4(147,36,52,255);
   match ip1 { // match &ip1 // match &mut ip1
      V4(a1,a2,a3,a4) => println!("{a1:?} {a2:?} {a3:?} {a4:?}"),
      V6(addr) => println!("{addr:?}") }
   let ip2 = V6(String::from("123.123.123.123.123.123"));
   match &ip2 {
      V4(a1,a2,a3,a4) => println!("{a1:?} {a2:?} {a3:?} {a4:?}"),
      V6(addr) => println!("{addr:?}") }
 }
