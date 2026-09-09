---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Overriding vs. Overloading
class foo_type(x: Int, y: Int) {
  val a : Int = x
  def b : Int = 0
  def f(z: Int) : Int = b * z
}
class gee_type(x: Int) extends foo_type(x+1,x+2) {
  def f(z: String) : Int = 77
}

Q: Can we override with a different type?
override def f(z: String): Int = 77         //No, arg: diff type
def f(z: String): Int = 77         // Overloading, arg: diff type
override def f(z: Int): Int = 77 //Yes, arg: same type
