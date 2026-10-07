---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 21
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
Complexity of Merge Sort
                                    '
                          Total = + 𝑛 − 2#$%
                                    #&%
Split the sum:
                              '           '
                            = + 𝑛 − + 2#$%
                              #&%         #&%
First term:
                          '
                       + 𝑛 = 𝑛 ⋅ 𝑚 = 𝑛 log 𝑛
                        #&%
Second term:
                      '
                      + 2#$% = 2' − 1 = 𝑛 − 1
                      #&%
                 Total comparisons = 𝑛 log 𝑛 − 𝑛 − 1
