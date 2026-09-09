---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 3
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Mutable Variables
➢Mutable Variables
  • Use “var” instead of “val” and “def”
  • We can update the value stored in a variable.

class Main(i: Int) {
  var a = i
}

val m = new Main(10)
m.a // 10
m.a = 20
m.a // 20
m.a += 5 // m.a = m.a + 5
m.a // 25
