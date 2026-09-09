---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 26
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Halting Problem
• Example: Can we develop a procedure that takes as input a computer program along with its
  input and determines whether the program will eventually halt with that input?
  – Answer: no

• Solution: Proof by contradiction.
  – Assume that there is such a procedure and call it H(P,I). The procedure H(P,I) takes as input a
   program P and the input I to P.
  – H outputs “halt” if it is the case that P will stop when run with input I.
  – Otherwise, H outputs “loops forever.”
