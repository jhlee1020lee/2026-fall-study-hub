---
course: "discrete_mathematics"
source_pdf: "03.Number.Theory.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf"
generated_at: "2026-09-20T23:38:11Z"
---
Probabilistic Test
• Def. A probabilistic test is an algorithm that determines whether a number is prime by
  using random choices.


• Example — Miller–Rabin Primality Test
The Miller–Rabin test is one of the most widely used probabilistic primality tests.

Procedure (simplified):
  – Choose a random number 𝑎.
  – Perform a modular exponentiation test.
  – If the test fails → 𝑛 is composite.
  – If it passes → 𝑛 is probably prime.
