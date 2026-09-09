---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Struct

 struct User {
    active: bool,
    name: String,
 }
 fn main() {
    println!("Size: {} bytes", std::mem::size_of::<User>());
    let mut user_name = String::from("gil");
    let mut u = User { active: true, name: user_name };
    u.name.push_str(" hur");
    println!("{}, {}", u.active, u.name);
    user_name = u.name;
    println!("{}, {}", u.active, user_name);
    // println!("{} {}", u.active, u.name);
 }
