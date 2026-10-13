---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bayesian Spam Filters
• Let S be the event that the message is spam, and E be the event that the message contains
  the word w. Using Bayes’ Rule,
                                             𝑝 𝐸 𝑆 𝑝(𝑆)
                            𝑝 𝑆 𝐸) =
                                     𝑝 𝐸 𝑆 𝑝 𝑆 +𝑝 𝐸 𝑆 𝑝 𝑆

• Assuming that it is equally likely that an arbitrary message is spam and is not spam; i.e.,
  p(S) = ½ .
  – Note: If we have data on the frequency of spam messages, we can obtain a better
    estimate for p(S).

                                                                      𝑝(𝑤)
• Using our empirical estimates of 𝑝 𝐸 𝑆 and 𝑝 𝐸 𝑆 : 𝑟 𝑤         =
                                                                   𝑝 𝑤 +𝑞 𝑤
  – r(w) estimates the probability that the message is spam. We can class the message as
   spam if r(w) is above a threshold.
