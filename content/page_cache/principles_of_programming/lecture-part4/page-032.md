---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 32
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Struct with lifetime annotation (Variations)
 struct Foo<'a,'b> {
    x: &'a i32,
    y: &'b i32,
 }

 fn main() {
   let x = 1;
   let v;
   {
      let y = 2;
      let f = Foo { x: &x, y: &y };
      v = f.x;
   }
   println!("{}", *v);
 }
