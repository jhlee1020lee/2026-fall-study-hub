---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bayesian Spam Filters
• Example: We find that the word “Rolex” occurs in 250 out of 2000 spam messages and
  occurs in 5 out of 1000 non-spam messages. Estimate the probability that an incoming
  message is spam. Suppose our threshold for rejecting the email is 0.9.

• Solution: p(Rolex) = 250/2000 =.0125 and q(Rolex) = 5/1000 = 0.005.
                                  𝑝(Rolex)               0.125
                𝑟 Rolex =                        =                 ≈ 0.962
                            𝑝 Rolex + 𝑞(Rolex) 0.125 + 0.005

• Hence we class the message as spam and reject the email!
