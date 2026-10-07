---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
 Quiz
Consider the recursive function:
def G(n):
  if n <= 1:
     return 1
  for i in range(n):
      x += 1
  return G(n/2) + G(n/4) + n
Assume 𝑛 is a power of 2.
What is the time complexity of 𝐺 𝑛 ?
• A. 𝑂 𝑛
• B. 𝑂 𝑛 log 𝑛
• C. 𝑂 𝑛%&'!(
• D. 𝑂 2!
