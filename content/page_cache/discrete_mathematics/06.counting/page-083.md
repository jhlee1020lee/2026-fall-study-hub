---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 83
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
Pascal’s Identity
• Pascal’s Identity: If n and r are integers with n ≥ r ≥ 0, then !#$
                                                                   3
                                                                      =    !
                                                                          3-$
                                                                                + !3
  –Start from the definition:
                  𝑛              𝑛!            𝑛       𝑛!
                        =                    ,   =
                𝑟−1        𝑟−1 ! 𝑛−𝑟+1 ! 𝑟         𝑟! 𝑛 − 𝑟 !
  –Put on a common denominator
  Rewrite the first term:
                              𝑛         𝑛! ⋅ 𝑟
                                  =
                             𝑟−1    𝑟! 𝑛 − 𝑟 + 1 !
  Rewrite the second term:
                              𝑛   𝑛! 𝑛 − 𝑟 + 1
                                =
                              𝑟   𝑟! 𝑛 − 𝑟 + 1 !
