---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Interface over Parameter Types
trait Ord[A] {
  def cmp(that: A): Int

  def ===(that: A): Boolean = (this.cmp(that)) == 0
  def < (that: A): Boolean = (this cmp that) < 0
  def > (that: A): Boolean = (this cmp that) > 0
  def <= (that: A): Boolean = (this cmp that) <= 0
  def >= (that: A): Boolean = (this cmp that) >= 0
}
def max3[A <: Ord[A]](a: A, b: A, c: A) : A =
  if (a <= b) {if (b <= c) c else b }
  else        {if (a <= c) c else a }

class OInt(val value : Int) extends Ord[OInt] {
  def cmp(that: OInt) = value - that.value
}
max3(new OInt(3), new OInt(2), new OInt(10)).value
