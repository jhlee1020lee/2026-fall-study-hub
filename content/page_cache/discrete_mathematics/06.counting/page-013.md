---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
 More Examples
• Recursive Modular Exponentiation: Devise a recursive algorithm for computing bn mod
  m, where b, n, and m are integers with m ≥ 2, n ≥ 0, and 1≤ b ≤ m.

           procedure mpower(b,m,n: integers with b > 0 and m ≥ 2, n ≥ 0)
                if n = 0 then return 1
                else if n is even then return mpower(b,n/2,m)2 mod m
                else return (mpower(b,⌊n/2⌋,m)2 mod m· b mod m) mod m
