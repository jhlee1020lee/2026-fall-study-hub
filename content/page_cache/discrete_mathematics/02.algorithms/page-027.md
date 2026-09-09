---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 27
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
  Halting Problem - proof
• Since a program is a string of characters, we can call H(P,P). Construct a procedure K(P), which
  works as follows.
  – If H(P,P) outputs “loops forever” then K(P) halts.
  – If H(P,P) outputs “halt” then K(P) goes into an infinite loop printing “ha” on each iteration.




• Now we call K with K as input, i.e. K(K).
  – If the output of H(K,K) is “loops forever” then K(K) halts. A Contradiction.
  – If the output of H(K,K) is “halts” then K(K) loops forever. A Contradiction.
• Therefore, the halting problem is unsolvable.
