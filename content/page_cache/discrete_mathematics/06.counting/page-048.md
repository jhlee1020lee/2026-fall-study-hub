---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 48
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
 Quiz
def G(n):
  if n <= 1:
     return 1
  for i in range(n):
      x += 1
  return G(n/2) + G(n/4) + n
• Build the Recursion Tree
  – Level 0 (root)
                                      𝑛
  – Level 1
  Two recursive calls:
  𝑇 𝑛/2 → contributes 𝑛/2
  𝑇 𝑛/4 → contributes 𝑛/4
  Total:
                               𝑛/2 + 𝑛/4 = 3𝑛/4
