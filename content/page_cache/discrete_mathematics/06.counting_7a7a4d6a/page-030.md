---
course: "discrete_mathematics"
source_pdf: "06.Counting_7a7a4d6a.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting_7a7a4d6a.pdf"
generated_at: "2026-10-13T03:36:28Z"
---
  Distributing Objects into Boxes
• Indistinguishable boxes.
   – There is no simple closed formula for the number of ways to distribute n distinguishable
    objects into j indistinguishable boxes.

  Example: The number of ways to partition a set of 𝑛 distinct elements into 𝑘 non-empty,
  indistinguishable subsets.（Stirling numbers of the second kind）
  Recurrence Formula: S(n,k)=k⋅S(n−1,k)+S(n−1,k−1)

  – The number of ways of distributing n indistinguishable objects into k indistinguishable
   boxes equals pk(n), the number of ways to write n as the sum of at most k positive integers
   in increasing order. No simple closed formula exists for this number.
