---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 24
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
  –Level 2
  Each node splits again:
  From 𝑛/2:
                                 𝑛/4 + 𝑛/8
  From 𝑛/4:
                                𝑛/8 + 𝑛/16
  Total:
                                                    3 )
                   𝑛/4 + 𝑛/8 + 𝑛/8 + 𝑛/16 = 9𝑛/16 =     𝑛
                                                    4
