---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Sub Types for Functions
• Function Sub Type
                      T <: T’ S <: S’
                 =======================
                     (T’=>S) <: (T=>S’)
• Example
import reflect.Selectable.reflectiveSelectable
def foo(s: {val a: Int; val b: Int}) : {val x: Int; val y: Int} = {
  object tmp {
    val x = s.b
    val y = s.a
  }
  tmp
}
val gee: {val a: Int; val b: Int; val c: Int} => {val x: Int} =
  foo _
