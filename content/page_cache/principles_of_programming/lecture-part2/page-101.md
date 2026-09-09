---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 101
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Intersection Types
Ø Typing Rule
                               t : T1 t: T2
                             =============
                               t : T1 with T2

Ø Example
trait A { val a: Int = 0 }
trait B { val b: Int = 0 }
class C extends A with B {
  override val a = 10
  override val b = 20
  val c = 30
}
val x = new C
val y: A with B = x
y.a // 10
y.b // 20
y.c // type error
