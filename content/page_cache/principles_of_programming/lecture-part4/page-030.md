---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Struct with lifetime annotation
 // Key Idea: Track the lifetime of each field of a struct separately.
 struct User<'a,'b> { name: &'a mut String, email: &'b String }
 fn main() {
    println!("Size: {} bytes", std::mem::size_of::<User>());
    let mut user_name = String::from("gil");
    let temp : &String;
    { let mut user_email = String::from("gil.hur@sf.snu.ac.kr");
       let mut u = User { name: &mut user_name, email: &user_email };
       u.name.push_str(" hur");
       println!("{}, {}", u.name, u.email);
       temp = u.name; // temp = u.email;
       // u.name.push_str("xxx");
    }
    println!("{}", temp);
 }
