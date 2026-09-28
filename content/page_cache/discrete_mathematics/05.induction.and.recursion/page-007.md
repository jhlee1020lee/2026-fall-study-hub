---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 7
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
 Strong Induction
• Strong Induction: To prove that P(n) is true for all positive integers n, where P(n) is a
  propositional function, complete two steps:
  – Basis Step: Verify that the proposition P(1) is true.
  – Inductive Step: Show the conditional statement
                          𝑃 1 ∧ 𝑃 2 ∧⋯∧𝑃 𝑘 → 𝑃 𝑘 +1
                    holds for all positive integers 𝑘.
• Now we assume that 𝑃 1 , … , 𝑃 𝑘 are all true, not just 𝑃 𝑘 . So the induction hypothesis
  is stronger.
• Example: Fundamental Theorem of Arithmetic
• There are other forms of mathematical induction; which form of induction should be used?
