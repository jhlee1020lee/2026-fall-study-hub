---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 25
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
  –Pattern
                           (
  Each level multiplies by ":
  Level 0: 𝑛
             (
  Level 1: 𝑛
             "
                 ( )
  Level 2:       "
                     𝑛
                 ( *
  Level k:           𝑛
                 "
