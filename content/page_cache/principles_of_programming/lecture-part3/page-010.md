---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Syntax for type class: syntactic sugar
trait Ord[A]:
  extension (self: A)
   def cmp(a: A): Int
   def ===(a: A) = self.cmp(a) == 0
   def < (a: A) = self.cmp(a) < 0
   def > (a: A) = self.cmp(a) > 0
   def <= (a: A) = self.cmp(a) <= 0
   def >= (a: A) = self.cmp(a) >= 0

def max3[A: Ord](a: A, b: A, c: A) : A =
 if (a <= b) { if (b <= c) c else b }
 else        { if (a <= c) c else a }

given intOrd : Ord[Int] with
 extension (self: Int)
   def cmp(a: Int) = self - a

max3(3,2,10) // 10
