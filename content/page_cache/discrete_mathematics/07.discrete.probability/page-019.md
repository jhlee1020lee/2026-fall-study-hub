---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bernoulli Trials
• Theorem: The probability of exactly k successes in n independent Bernoulli trials, with
  probability of success p and probability of failure q = 1 − p, is C(n,k)pkqn−k.
• Proof: The outcome of n Bernoulli trials is an n-tuple (t1,t2,…,tn), where each is ti either S
  (success) or F (failure). The probability of each outcome of n trials consisting of k successes
  and k − 1 failures (in any order) is pkqn−k. Because there are C(n,k) n-tuples of S’s and F’s
  that contain exactly k S’s, the probability of k successes is C(n,k)pkqn−k.

• We denote by b(k:n,p) the probability of k successes in n independent Bernoulli trials with
  p the probability of success. Viewed as a function of k, b(k:n,p) is the binomial distribution.
  By Theorem, b(k:n,p) = C(n,k)pkqn−k.
