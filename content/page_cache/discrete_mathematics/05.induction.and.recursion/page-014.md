---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
Length of a String
• Example: Give a recursive definition of 𝑙 𝑤 , the length of the string 𝑤.

• Solution: The length of a string can be recursively defined by:
  BASIS STEP: 𝑙 𝜆 = 0
  RECURSIVE STEP: If 𝑤 is in Σ ∗ and 𝑥 is in Σ, then 𝑙 𝑤𝑥 = 𝑙 𝑤 + 1


• Theorem: 𝑙 𝑥𝑦 = 𝑙 𝑥 + 𝑙 𝑦 for any 𝑥, 𝑦 ∈ Σ ∗
