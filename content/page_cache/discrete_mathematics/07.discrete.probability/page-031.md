---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bayesian Spam Filters using Multiple Words
• Accuracy can be improved by considering more than one word as evidence.
• Consider the case where E1 and E2 denote the events that the message contains the words
  w1 and w2 respectively.
• We make the simplifying assumption that the events are independent. And again we
  assume that p(S) = ½ . Then,
                                             𝑝 𝐸1 𝑆 𝑝 𝐸2 𝑆
                    𝑝 𝑆 𝐸1 ∩ 𝐸2 =
                                    𝑝 𝐸1 𝑆 𝑝 𝐸2 𝑆 + 𝑝 𝐸1 𝑆 𝑝 𝐸2 𝑆

                                            𝑝 𝑤1 𝑝 𝑤2
                        𝑟 𝑤1 , 𝑤2   =
                                      𝑝 𝑤1 𝑝 𝑤2 + 𝑞 𝑤1 𝑞 𝑤2
