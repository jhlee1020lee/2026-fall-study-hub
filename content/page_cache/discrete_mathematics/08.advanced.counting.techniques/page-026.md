---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 26
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
 Derangements
• The Hatcheck Problem: A new employee checks the hats of n people at restaurant,
  forgetting to put claim check numbers on the hats. When customers return for their hats,
  the checker gives them back hats chosen at random from the remaining hats. What is the
  probability that no one receives the correct hat.

• Solution: The answer is the number of ways the hats can be arranged so that there is no
  hat in its original position divided by n!, the number of permutations of n hats.

• Remark: It can be shown that the probability of a derangement approaches 1/e as n grows
  without bound.

                        1          1 1         𝑛
                                                 1     −1
                           𝐷𝑛 = 1 − + − ⋯ + −1      →𝑒
                        𝑛!         1! 2!         𝑛!
