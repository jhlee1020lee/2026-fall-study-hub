---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 40
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Average-Case Complexity of Linear Search
• Example: Describe the average case performance of the linear search algorithm.
  Assume the element is in the list and that the possible positions are equally likely.

• Solution: By the argument on the previous slide, if x = ai , the number of comparisons
  is 2i + 1.
                           3 + 5 + ⋯ + (2𝑛 + 1)
                                                    =𝑛+2
                                      𝑛

 Hence, the average-case complexity is Θ(n).
