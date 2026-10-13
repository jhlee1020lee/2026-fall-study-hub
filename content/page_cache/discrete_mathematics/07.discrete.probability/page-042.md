---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 42
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
  Variance
• Bienaymé‘s Formula: If X and Y are two independent random variables on a sample space
  S, then V(X + Y) = V(X) + V(Y). Furthermore, if Xi, i = 1,2, …,n, with n a positive integer, are
  pairwise independent random variables on S, then
                        𝑉 𝑋1 + 𝑋2 + ⋯ + 𝑋𝑛 = 𝑉 𝑋1 + ⋯ + 𝑉 𝑋𝑛


• Example: Find the variance of the number of successes when n independent Bernoulli
  trials are performed, where on each trial, p is the probability of success and q is the
  probability of failure.
  – Let Xi be the random variable with Xi ((t1, t2, …., tn)) = 1 if trial ti is a success and Xi ((t1, t2, …., tn)) =
   0 if it is a failure. Let X = X2 + X3 + …. Xn. Then X counts the number of successes in the n trials.
  – By Bienaymé ‘s Formula, it follows that V(X)= V(X1) + V(X2) + ∙∙∙ + V(Xn) and V(Xi) = pq
