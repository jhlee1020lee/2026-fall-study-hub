---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 99
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
  Distributing Objects into Boxes
• Indistinguishable boxes.
   – There is no simple closed formula for the number of ways to distribute n distinguishable
    objects into j indistinguishable boxes.
   –Example: The number of ways to partition a set of 𝑛 distinct elements into 𝑘 non-empty,
    indistinguishable subsets.（Stirling numbers of the second kind）
    Partition 𝑎 𝑏 𝑐 into 2 groups:
    {a,b} | {c}
    {a,c} | {b}
    {b,c} | {a}
                                       𝑆 3 2 =3
  –Recurrence Formula: S(n,k)=k⋅S(n−1,k)+S(n−1,k−1)
