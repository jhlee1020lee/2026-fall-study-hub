---
course: "discrete_mathematics"
source_pdf: "06.Counting_7a7a4d6a.pdf"
pdf_page: 28
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting_7a7a4d6a.pdf"
generated_at: "2026-10-13T03:36:28Z"
---
Permutations with Indistinguishable Objects
• Example: How many different strings can be made by reordering the letters of the word
  SUCCESS.

• Thm: The number of different permutations of n objects, where there are n1
  indistinguishable objects of type 1, n2 indistinguishable objects of type 2, …., and nk
  indistinguishable objects of type k, is:
                                               𝑛!
                                         𝑛1 ! 𝑛2 ! … 𝑛𝑘 !

• Proof: By the product rule the total number of permutations is:
                    C(n, n1) C(n − n1, n2 ) ∙∙∙ C(n − n1 − n2 − ∙∙∙ − nk, nk)
  – Why?
