---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
Birthday Paradox
• The puzzle of finding the number of people needed in a room to ensure that the
  probability of at least two of them having the same birthday is more than ½ has a
  surprising answer, which we now find.
  – It is a “paradox” not because of a logical contradiction, but because it goes against intuition


• Solution: We assume that all birthdays are equally likely and that there are 366 days in
  the year. First, we find the probability pn that at least two of n people have different
  birthdays.
  – pn = (365/366)(364/366)∙∙∙ (367 − n)/366.
  – Therefore , 1− pn = 1−(365/366)(364/366)∙∙∙ (367 − n)/366.

• Checking various values for n with computation help tells us that for n = 22, 1− pn ≈ 0.457,
  and for n = 23, 1− pn ≈ 0.506. Consequently, a minimum number of 23 people are needed
  so that that the probability that at least two of them have the same birthday is greater
  than 1/2.
