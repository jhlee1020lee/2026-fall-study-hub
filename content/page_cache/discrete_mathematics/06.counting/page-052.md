---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 52
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
 Quiz
Consider the recursive function:
def G(n):
  if n <= 1:
     return 1
return G(n/2) + G(n/4) + n
What is the time complexity of 𝐺 𝑛 ?
 –The running time is governed by the number of recursive calls, and satisfies
                       𝑇 𝑛 = 𝑇 𝑛/2 + 𝑇 𝑛/4 + 𝑂 1 .
 Its solution is
                                 𝑇 𝑛 = Θ 𝑛, ,
