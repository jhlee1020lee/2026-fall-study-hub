---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
 Validity of Mathematical Induction
• Mathematical induction is valid because of the well ordering property, which states that
  every nonempty subset of the set of positive integers has a least element. Here is the proof:
  – Suppose that P(1) holds and P(k) → P(k + 1) is true for all positive integers k.
  – Assume there is at least one positive integer n for which P(n) is false. Then the set S of positive
   integers for which P(n) is false is nonempty.
  – By the well-ordering property, S has a least element, say m.
  – We know that m can not be 1 since P(1) holds.
  – Since m is positive and greater than 1, m − 1 must be a positive integer. Since m − 1 < m, it is
   not in S, so P(m − 1) must be true.
  – But then, since the conditional P(k) → P(k + 1) for every positive integer k holds, P(m) must
   also be true. This contradicts P(m) being false.
  – Hence, P(n) must be true for every positive integer n.
