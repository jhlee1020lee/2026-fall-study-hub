---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 51
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
   – Total work:
                                         3  3 (
                                𝑇 𝑛 =𝑛 1+ +     +⋯
                                         4  4
                                            )
  This is a geometric series with ratio 𝑟 = *.
  So:
                                              1
                               𝑇 𝑛 ≤𝑛⋅             = 𝑛 ⋅ 4 = 4𝑛
                                           1 − 3/4

                                          𝑇 𝑛 =𝑂 𝑛
