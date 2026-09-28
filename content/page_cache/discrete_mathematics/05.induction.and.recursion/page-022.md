---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
 More Examples
• Recursive GCD: Give a recursive algorithm for computing the greatest common divisor of
  two nonnegative integers a and b with a < b.

             procedure gcd(a,b: nonnegative integers with a < b)
                  if a = 0 then return b
                  else return gcd (b mod a, a)

• Recursive Modular Exponentiation: Devise a a recursive algorithm for computing bn
  mod m, where b, n, and m are integers with m ≥ 2, n ≥ 0, and 1≤ b ≤ m.

             procedure mpower(b,m,n: integers with b > 0 and m ≥ 2, n ≥ 0)
                  if n = 0 then return 1
                  else if n is even then return mpower(b,n/2,m)2 mod m
                  else return (mpower(b,⌊n/2⌋,m)2 mod m∙ b mod m) mod m
