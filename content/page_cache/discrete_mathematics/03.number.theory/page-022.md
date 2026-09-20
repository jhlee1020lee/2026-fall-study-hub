---
course: "discrete_mathematics"
source_pdf: "03.Number.Theory.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf"
generated_at: "2026-09-20T23:38:11Z"
---
The Euclidean Algorithm
• The Euclidean algorithm expressed in pseudocode is:

             procedure gcd(a, b: positive integers)
                 x := a
                 y := b
                 while y ≠ 0
                       r := x mod y
                       x := y
                       y := r
                 return x {gcd(a,b) is x}


• Correctness?
• The time complexity of the algorithm is 𝑂 log 𝑏 divisions.
