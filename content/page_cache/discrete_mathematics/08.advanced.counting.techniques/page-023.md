---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
 The Principle of Inclusion-Exclusion
• Theorem. The Principle of Inclusion-Exclusion: Let A1, A2, …, An be finite sets. Then:


                                                                                 𝑛−1
     𝐴1 ∪ 𝐴2 ∪ ⋯ ∪ 𝐴𝑛 = ෍ 𝐴𝑖 −                       ෍     𝐴𝑖 ∩ 𝐴𝑗 + ⋯ + −1            𝐴1 ∩ ⋯ ∩ 𝐴𝑛
                                    1≤𝑖≤𝑛        1≤𝑖<𝑗≤𝑛


• Proof idea: An element in the union is counted exactly once in the right-hand side of the
  equation. Consider an element a that is a member of r of the sets A1,…., An where 1≤ r ≤ n.
                    𝑟
  – It is counted   1
                        times by σ1≤𝑖≤𝑛 𝐴𝑖
                    𝑟
  – It is counted   2
                        times by σ1≤𝑖<𝑗≤𝑛 𝐴𝑖 ∩ 𝐴𝑗
                                𝑟
  – In general, it is counted   𝑘
                                    times by the summation of k of the sets Ai
                                             𝑟       𝑟             𝑟−1 𝑟
  – This, the element is counted exactly     1
                                                 −   2
                                                         + ⋯+   −1     𝑟
                                                                           = 1 times
