---
course: "discrete_mathematics"
source_pdf: "06.Counting_7a7a4d6a.pdf"
pdf_page: 26
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting_7a7a4d6a.pdf"
generated_at: "2026-10-13T03:36:28Z"
---
Combinations with Repetitions
• Thm: The number of r-combinations from a set with n elements when repetition of
                         𝑛+𝑟−1
  elements is allowed is   𝑟
                               .

• Proof: Each r-combination of a set with n elements with repetition allowed can be
  represented by a list of n –1 bars and r stars. The bars mark the n cells containing a star
  for each time the ith element of the set occurs in the combination.

• The number of such lists is C(n + r – 1, r), because each list is a choice of the r positions
  to place the stars, from the total of n + r – 1 positions to place the stars and the bars.
  This is also equal to C(n + r – 1, n –1), which is the number of ways to place the n –1
  bars.

• Remark: This is the number of solutions of the equation 𝑥1 + ⋯ + 𝑥𝑛 = 𝑟, where 𝑥𝑖 ’s
  are nonnegative integers.
