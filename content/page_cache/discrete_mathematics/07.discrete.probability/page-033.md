---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Bayesian Spam Filters using Multiple Words
• In general, the more words we consider, the more accurate the spam filter. With
  the independence assumption if we consider k words:

                       𝑘
                                                 ς𝑘𝑖=1 𝑝(𝐸𝑖 |𝑆)
                  𝑝 𝑆 ⋂𝑖=1 𝐸𝑖        =
                                         ς𝑘𝑖=1 𝑝(𝐸𝑖 |𝑆) + ς𝑘𝑖=1 𝑝 𝐸𝑖 𝑆
                                              𝑘
                                            ς𝑖=1 𝑝 𝑤𝑖
                     𝑝 𝑤1 , … , 𝑤𝑘   = 𝑘             𝑘
                                      ς𝑖=1 𝑝(𝑤𝑖 ) + ς𝑖=1 𝑞(𝑤𝑖 )

• We can further improve the filter by considering pairs of words as a single block
  or certain types of strings.
