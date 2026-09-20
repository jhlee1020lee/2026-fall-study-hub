---
course: "discrete_mathematics"
source_pdf: "03.Number.Theory.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf"
generated_at: "2026-09-20T23:38:11Z"
---
GCDs as Linear Combination
• Bézout’s Theorem: If a and b are positive integers, then there exist integers s and t such
  that gcd(a,b) = sa + tb. Such integers s and t are called Bézout coefficients.


• Example: find 𝑠, 𝑡 such that gcd 252, 198 = 252𝑠 + 198𝑡
  – (Forward) The Euclidean algorithm
                        252 = 198 ⋅ 1 + 54 ⇒ 54 = 252 − 1 ⋅ 198
                         198 = 54 ⋅ 3 + 36 ⇒ 36 = 198 − 3 ⋅ 54
                           54 = 36 ⋅ 1 + 18 ⇒ 18 = 54 − 1 ⋅ 36
                           36 = 18 ⋅ 2 + 0
  – (Backward)
                 18 = 54 − 1 ⋅ 36 = 54 − 1 ⋅ 198 − 3 ⋅ 54 = 54 ⋅ 4 − 198
                    = 252 − 1 ⋅ 198 ⋅ 4 − 198 = 252 ⋅ 4 + 198 ⋅ −5
  – There is a one-pass method, called the extended Euclidean algorithm.
