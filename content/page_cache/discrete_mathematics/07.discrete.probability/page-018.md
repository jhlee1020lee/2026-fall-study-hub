---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bernoulli Trials
• Definition: Suppose an experiment can have only two possible outcomes, e.g., the flipping
  of a coin or the random generation of a bit.
  – Each performance of the experiment is called a Bernoulli trial.
  – One outcome is called a success and the other a failure.
  – If p is the probability of success and q the probability of failure, then p + q = 1.


• Example: A coin is biased so that the probability of heads is 2/3. What is the probability
  that exactly four heads occur when the coin is flipped seven times?
• Solution: There are 27 = 128 possible outcomes. The number of ways four of the seven
  flips can be heads is C(7,4). The probability of each of the outcomes is (2/3)4(1/3)3 since
  the seven flips are independent. Hence, the probability that exactly four heads occur is
           C(7,4) (2/3)4(1/3)3 = (35∙ 16)/ 27 = 560/ 2187.
