---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
For loop
➢For loop
  • Syntax: for (i <- collection) body
    Executes body for each i in collection.
  • It is equivalent to:

   def myfor[A](xs: Traversable[A])(f: A => Unit) : Unit =
     xs.foreach(f)

➢Example
var sum = 0
for (i <- 0 to 100 by 2) { // myfor (0 to 100 by 2) { i =>
  sum += i
}
sum // 2550
