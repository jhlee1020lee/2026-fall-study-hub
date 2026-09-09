---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
While loop
➢While loop
  • Syntax: while (cond) body
    Executes body while cond holds.
  • It is equivalent to:

   def mywhile(cond: =>Boolean)(body: =>Unit) : Unit =
     if (cond) { body; mywhile(cond)(body) } else ()

➢Example
var i = 0
var sum = 0
while (i <= 100) { // mywhile (i <= 100) {
  sum += i
  i += 2
}
sum // 2550
