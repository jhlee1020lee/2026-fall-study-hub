---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Implicit
ØImplicit
  • An argument is given “implicitly”

def foo(s: String)(implicit t: String) = s + t

implicit val exclamation : String = "!!!!!!"

foo("Hi")
foo("Hi")("???") // can give it explicitly
