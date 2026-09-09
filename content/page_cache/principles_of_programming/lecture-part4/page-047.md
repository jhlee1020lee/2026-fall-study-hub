---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 47
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Dyn: dynamic dispatch
 impl Describable for i64 {
    fn describe(&self) -> String {
      format!("64-bit-signed-integer: {}", *self)
    }
  }

 fn main() {
   let book = Book{title: "PP".to_string(), author: "Gil Hur".to_string()};
   let ds : Vec<Box<dyn Describable>> =
      vec![Box::new(42), Box::new(book)];
   for d in &ds {
      println!("{}", d.describe())
      // cannot use print_desc : why?
   }
 }
