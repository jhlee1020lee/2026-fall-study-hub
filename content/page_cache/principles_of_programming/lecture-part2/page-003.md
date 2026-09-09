---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 3
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Motivation
We want:
object tom {
  val name = "Tom"
  val home = "02-880-1234"
}
object bob {
  val name = "Bob"
  val mobile = "010-1111-2222"
}
def greeting(r: ???) = "Hi " + r.name + ", How are you?"
greeting(tom)
greeting(bob)
Note that we have
tom: {val name: String; val home: String}
bob: {val name: String; val mobile: String}
