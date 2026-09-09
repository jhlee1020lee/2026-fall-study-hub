---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Struct with lifetime annotation (Variations)
 // Key Idea: Track the lifetime of each field of a struct separately.
 // Easy to understand if you inline the definition of a struct.
 struct User1<'a> {
  name: &'a String,
  email: &'a String }
 // User1 : for <'a> fn(&'a String, &'a String) : User1<'a>
 // User1::name : for <'a> fn(User1<'a>) : &'a String
 // User1::email : for <'a> fn(User1<'a>) : &'a String

 struct User2<'a,'b> {
  user: User1<'a>,
  addr: &'b String }
 // User2 : for <'a,'b> fn(User1<'a>, &’b String) : User2<'a,'b>
 // User2::user : for <'a,'b> fn(User2<'a,'b>) : User1<'a>
 // User2::addr : for <'a,'b> fn(User2<'a,'b>) : &'b String
