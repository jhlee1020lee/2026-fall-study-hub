---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 28
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bayesian Spam Filters
• How do we develop a tool for determining whether an email is likely to be spam?

• If we have an initial set B of spam messages and set G of non-spam messages. We can use
  this information along with Bayes’ law to predict the probability that a new email message
  is spam.

• We look at a particular word w, and count the number of times that it occurs in B and in G;
  nB(w) and nG(w).
  – Estimated probability that a spam message contains w is: p(w) = nB(w)/|B|
  – Estimated probability that a message that is not spam contains w is: q(w) = nG(w)/|G|
