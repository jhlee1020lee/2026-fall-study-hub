---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 46
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Type class
 trait Describable {
   fn describe(&self) -> String;
 }
 struct Book { title: String, author: String, }
 impl Describable for Book {
    fn describe(&self) -> String {
       format!("{} by {}", self.title, self.author)
    }}

 //fn print_desc(a: &impl Describable) -> ()
 fn print_desc<T>(a: &T) -> () where T : Describable
 { println!("{}", a.describe()) }
 fn main() {
    print_desc(&Book{title: "PP".to_string(), author: "Gil Hur".to_string()})
 }
