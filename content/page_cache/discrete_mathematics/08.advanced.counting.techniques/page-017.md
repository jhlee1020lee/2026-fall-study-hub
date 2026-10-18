---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 17
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
  Divide-and-Conquer Recurrence Relations
• Suppose that a recursive algorithm divides a problem of size n into a subproblems. Assume
  each subproblem is of size n/b. Suppose g(n) extra operations are needed in the conquer
  step. Then f(n) represents the number of operations to solve a problem of size n satisfies
  the following recurrence relation:
                                   𝑓 𝑛 = 𝑎𝑓 𝑛/𝑏 + 𝑔 𝑛
  – This is called a divide-and-conquer recurrence relation.


• Examples
  – Binary search: 𝑓 𝑛 = 𝑓 𝑛Τ2 + 1
  – Merge sort: 𝑓 𝑛 = 2𝑓 𝑛Τ2 + 𝑛
