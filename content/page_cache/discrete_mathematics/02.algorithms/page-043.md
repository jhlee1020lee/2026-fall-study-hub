---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Complexity of Matrix Multiplication
• How many additions of integers and multiplications of integers are used by the matrix
  multiplication algorithm to multiply two n x n matrices?

• There are n2 entries in the product. Finding each entry requires n multiplications and
  (n − 1) additions. Hence, n3 multiplications and n2(n − 1) additions are used.

• Hence, the complexity of matrix multiplication is O(n3).

• Surprisingly, algorithms exist that provide better running times than this
  straightforward "schoolbook algorithm".
