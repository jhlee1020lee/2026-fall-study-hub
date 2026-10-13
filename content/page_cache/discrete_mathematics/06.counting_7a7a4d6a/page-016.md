---
course: "discrete_mathematics"
source_pdf: "06.Counting_7a7a4d6a.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting_7a7a4d6a.pdf"
generated_at: "2026-10-13T03:36:28Z"
---
 The Number of Permutations
• Thm: If n is a positive integer and r is an integer with 1 ≤ r ≤ n, then there are
          P(n, r) = n(n − 1)(n − 2) ∙∙∙ (n − r + 1) = n! / (n - r)!
   r-permutations of a set with n distinct elements.

• Proof: Use the product rule. The first element can be chosen in n ways. The second in n − 1
  ways, and so on until there are (n − (r − 1)) ways to choose the last element.

• Note that P(n,0) = 1, since there is only one way to order zero elements (empty
  permutation). The formula P(n, r) = n! / (n - r)! Still applies.

• Examples : How many ways are there to select a first-prize winner, a second-prize winner,
  and a third-prize winner from 10 different people who have entered a contest?
