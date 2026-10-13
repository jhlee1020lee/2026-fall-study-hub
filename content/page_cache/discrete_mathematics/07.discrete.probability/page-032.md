---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 32
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bayesian Spam Filters using Multiple Words
• Example: We have 2000 spam messages and 1000 non-spam messages. The word
  “stock” occurs 400 times in the spam messages and 60 times in the non-spam.
  The word “undervalued” occurs in 200 spam messages and 25 non-spam.
  Estimate the probability that an incoming message is spam given that it contains
  both w1: “stock” and w2: “undervalued”.

• Solution: p(w1) = 0.2, q(w1) = 0.06, p(w2) = 0.1, q(w2) = 25/1000 = 0.025
                                        (0.2)(0.1)
                 𝑟 𝑤1 , 𝑤2 =                                 ≈ 0.930
                                0.2 0.1 + 0.06 0.025

  – If our threshold is 0.9, then we class the message as spam and reject it
