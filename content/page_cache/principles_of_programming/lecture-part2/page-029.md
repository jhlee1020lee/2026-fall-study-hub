---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Overriding
class foo_type(x: Int, y: Int) {
  val a : Int = x
  def b : Int = 0
  def f(z: Int) : Int = b * z
}
class gee_type(x: Int) extends foo_type(x+1,x+2) {
 override def b = 10
 // or, override def b = super.b + 10
 val c : Int = f(x) + b
}

(new gee_type(30)).c
def test(v: foo_type) =
 println(v.f(42))
test(new foo_type(1,2))
test(new gee_type(0))
