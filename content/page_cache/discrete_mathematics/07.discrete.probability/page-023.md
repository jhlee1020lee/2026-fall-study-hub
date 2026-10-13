---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Derivation of Bayes’ Theorem
• Bayes’ Theorem: Suppose that E and F are events from a sample space S such that p(E)≠ 0
  and p(F) ≠ 0. Then:
                                            𝑝 𝐸 𝐹) 𝑝(𝐹)
                        𝑝 𝐹 𝐸) =
                                    𝑝 𝐸 𝐹) 𝑝 𝐹 + 𝑝 𝐸 𝐹)𝑝 𝐹


• Lemma: 𝑝 𝐸 = 𝑝 𝐹 𝑝 𝐸 𝐹 + 𝑝 𝐹 𝑝 𝐸 𝐹
  – Note that 𝑝 𝐸 = 𝑝 𝐸 ∩ 𝐹 + 𝑝 𝐸 ∩ 𝐹
  – From 𝑝 𝐸 ∩ 𝐹 = 𝑝 𝐸 𝐹) 𝑝 𝐹 = 𝑝 𝐹 𝐸) 𝑝 𝐸 , we have
                                         𝑝 𝐹 𝑝(𝐸|𝐹)
                                𝑝 𝐹 𝐸) =
                                            𝑝 𝐸
