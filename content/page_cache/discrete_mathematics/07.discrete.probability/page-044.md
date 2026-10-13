---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 44
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Chebyshev’s Inequality
• Chebyschev’s Inequality: Let X be a random variable on a sample space S with
  probability function p. If r is a positive real number, then
                                                            1
                                 𝑝 𝑋 𝑠 − 𝐸 𝑋 ≥ 𝑟 ≤ 2 𝑉(𝑋)
                                                            𝑟

• Example: Suppose that X is a random variable that counts the number of tails when a fair
  coin is tossed n times.
  – X is the number of successes when n independent Bernoulli trials, each with probability of success
   ½ are done. Hence, E(X) = n/2 and V(X) = n/4.
  – By Chebyschev’s inequality with 𝑟 = 𝑛, 𝑝 𝑋 𝑠 − 𝑛Τ2 ≥ 𝑛 ≤ 𝑛/4 Τ               𝑛 2 = 1Τ4.
  – This means that the probability that the number of tails that come up on n tosses deviates from
   the mean , n/2, by more than √n is no larger than ¼ .
