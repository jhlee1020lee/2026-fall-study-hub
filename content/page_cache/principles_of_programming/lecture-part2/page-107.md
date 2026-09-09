---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 107
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
IntStack: Custom Modifications
ØCUSOM

trait Doubling extends Stack[Int] {
  abstract override def put(x: Int): Stack[Int] = super.put(2 * x)
}

trait Incrementing extends Stack[Int] {
  abstract override def put(x: Int): Stack[Int] = super.put(x + 1)
}

trait Filtering extends Stack[Int] {
  abstract override def put(x: Int): Stack[Int] =
    if (x >= 0) super.put(x) else this
}
