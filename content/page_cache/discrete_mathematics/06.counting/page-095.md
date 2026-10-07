---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 95
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
Combinations with Repetitions
• Thm: The number of r-combinations from a set with n elements when repetition of
  elements is allowed is !#3-$
                           3
                               .

• Proof: Each r-combination of a set with n elements with repetition allowed can be
  represented by a list of n –1 bars and r stars. The bars mark the n cells containing a star
  for each time the ith element of the set occurs in the combination.

• The number of such lists is C(n + r – 1, r), because each list is a choice of the r positions
  to place the stars, from the total of n + r – 1 positions to place the stars and the bars.
  This is also equal to C(n + r – 1, n –1), which is the number of ways to place the n –1
  bars.

• Remark: This is the number of solutions of the equation 𝑥$ + ⋯ + 𝑥! = 𝑟, where 𝑥/ ’s
  are nonnegative integers.
