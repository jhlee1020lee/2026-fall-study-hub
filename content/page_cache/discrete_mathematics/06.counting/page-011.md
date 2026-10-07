---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
 More Examples
• Recursive GCD: Give a recursive algorithm for computing the greatest common divisor of
  two nonnegative integers a and b with a < b.

             procedure gcd(a,b: nonnegative integers with a < b)
                  if a = 0 then return b
                  else return gcd (b mod a, a)
