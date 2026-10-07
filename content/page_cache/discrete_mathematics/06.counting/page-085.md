---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 85
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
Pascal’s Identity
• Pascal’s Identity: If n and k are integers with n ≥ k ≥ 0, then !#$
                                                                   3
                                                                      =    !
                                                                          3-$
                                                                                + !3
                                           𝑛+1
                                              𝑟
  = number of ways to choose r elements from 𝑛 + 1
  Pick one distinguished element (call it A).
  – Case 1: A is included
  We must choose r−1 more elements from the remaining 𝑛
                                              𝑛
                                           𝑟−1
  – Case 2: A is NOT included
  Choose all 𝑟 elements from the remaining 𝑛
                                              𝑛
                                              𝑟
  – Combine both cases
                                          𝑛       𝑛
                                                +
                                       𝑟−1        𝑟
