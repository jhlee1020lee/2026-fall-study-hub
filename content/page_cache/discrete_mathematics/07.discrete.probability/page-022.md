---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bayes’ Theorem
• Bayes’ Theorem: Suppose that E and F are events from a sample space S such that p(E)≠ 0
  and p(F) ≠ 0. Then:
                                            𝑝 𝐸 𝐹) 𝑝(𝐹)
                        𝑝 𝐹 𝐸) =
                                    𝑝 𝐸 𝐹) 𝑝 𝐹 + 𝑝 𝐸 𝐹)𝑝 𝐹

• Example: We have two boxes. The first box contains two green balls and seven red balls.
  The second contains four green balls and three red balls.
  Bob selects one of the boxes at random. Then he selects a ball from that box at random. If
  he has a red ball, what is the probability that he selected a ball from the first box.
   – Let E be the event that Bob has chosen a red ball and F be the event that Bob has
    chosen the first box.
   – By Bayes’ theorem the probability that Bob has picked the first box is:
                                      (7/9)(1/2)               49
                    𝑝 𝐹𝐸 =                                  =     ≈ 0.645
                                 7/9 (1/2) + (3/7)(1/2) 76
