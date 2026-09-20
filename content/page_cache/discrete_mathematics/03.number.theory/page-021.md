---
course: "discrete_mathematics"
source_pdf: "03.Number.Theory.pdf"
pdf_page: 21
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf"
generated_at: "2026-09-20T23:38:11Z"
---
The Euclidean Algorithm
• An efficient method for computing the GCD of two integers. It is based on the idea that
 gcd(a,b) is equal to gcd(b,r) when a > b and r is the remainder when a is divided by b.


• Example: Find gcd(91, 287).
                                   287 = 91 ⋅ 3 + 14
                                     91 = 14 ⋅ 6 + 7
                                     14 = 7 ⋅ 2 + 0
              Hence, gcd 287, 91 = gcd 91, 14 = gcd 14, 7 = 7.
