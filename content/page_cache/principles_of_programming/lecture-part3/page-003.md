---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 3
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Subtype Polymorphism
trait Ord {
  // this cmp that < 0 iff this < that
  // this cmp that > 0 iff this > that
  // this cmp that == 0 iff this == that
  def cmp(that: Ord): Int

  def ===(that: Ord): Boolean = (this.cmp(that)) == 0
  def < (that: Ord): Boolean = (this cmp that) < 0
  def > (that: Ord): Boolean = (this cmp that) > 0
  def <= (that: Ord): Boolean = (this cmp that) <= 0
  def >= (that: Ord): Boolean = (this cmp that) >= 0
}
def max3(a: Ord, b: Ord, c: Ord) : Ord =
  if (a <= b) { if (b <= c) c else b }
  else        { if (a <= c) c else a }

* Problem: hard (almost impossible) to implement Ord (e.g., using Int)
