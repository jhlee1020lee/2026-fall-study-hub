---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Insertion Sort
• Insertion sort begins with the 2nd element. It
  compares the 2nd element with the 1st and puts it       procedure insertion sort
  before the first if it is not larger.                   (a1,…,an: real numbers with n ≥ 2)
                                                              for j := 2 to n
• Next the 3rd element is put into the correct position              i := 1
  among the first 3 elements.                                        while (aj > ai )
                                                                            i := i + 1
• In each subsequent pass, the n+1st element is put                  m := aj
  into its correct position among the first n+1                      for (k := 0 to j − i − 1)
  elements.                                                                 aj-k := aj-k-1
                                                                     ai := m
• Linear search is used to find the correct position.
