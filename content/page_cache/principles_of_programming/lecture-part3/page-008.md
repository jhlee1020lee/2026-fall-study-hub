---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Separating Functions from Data
trait Ord[A] {
  def cmp(self: A)(a: A): Int

    def ===(self: A)(a: A) = cmp(self)(a) == 0
    def < (self: A)(a: A) = cmp(self)(a) < 0
    def > (self: A)(a: A) = cmp(self)(a) > 0
    def <= (self: A)(a: A) = cmp(self)(a) <= 0
    def >= (self: A)(a: A) = cmp(self)(a) >= 0
}

def max3[A](a: A, b: A, c: A)(implicit ORD: Ord[A]) : A =
  if (ORD.<=(a)(b)) {if (ORD.<=(b)(c)) c else b }
  else              {if (ORD.<=(a)(c)) c else a }

// behaves like Int <: Ord in OOP
implicit val intOrd : Ord[Int] = new {
   def cmp(self: Int)(a: Int) = self - a }
max3(3,2,10) // 10
