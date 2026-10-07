---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 20
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
Complexity of Merge Sort
From the earlier fact:
  Merging two lists of size 𝑎 and 𝑏 takes at most 𝑎 + 𝑏 − 1 comparisons
At level 𝑖:
Number of lists = 2# , with total size as n
Number of merges = 2#$%
So comparisons at level 𝑖:
                                            𝑛 − 2#$%
We sum from bottom to top (levels 𝑖 = 1 to 𝑚):
                                           '
                                  Total = + 𝑛 − 2#$%
                                          #&%
– Split the sum:
                   '
– = ∑'
     #&% 𝑛 − -#&% 2
                   #$%
