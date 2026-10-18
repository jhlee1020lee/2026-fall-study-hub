---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
 Estimating the Size of Divide-and-Conquer Functions
• Theorem: Let 𝑓 be an increasing function that satisfies the recurrence relation 𝑓 𝑛 =
  𝑎𝑓 𝑛/𝑏 + 𝑐 whenever n is divisible by b, where a≥ 1, b is an integer greater than 1, and c
  is a positive real number. Then, 𝑓 𝑛 is 𝑂 𝑛log𝑏 𝑎 if 𝑎 > 1, and 𝑂 log 𝑛 if 𝑎 = 1.
  Furthermore, , when n = bk and a ≠1, where k is a positive integer, 𝑓 𝑛 = 𝐶1 𝑛log𝑏 𝑎 + 𝐶2
  where 𝐶1 = 𝑓(1) + 𝑐/(𝑎 − 1) and 𝐶2 = −𝑐/(𝑎 − 1).

• Master Theorem: Let 𝑓 be an increasing function that satisfies the recurrence relation
                         𝑑                   𝑘
  𝑓 𝑛 = 𝑎𝑓 𝑛/𝑏 + 𝑐𝑛 whenever 𝑛 = 𝑏 , where 𝑘 is a positive integer, 𝑎 ≥ 1, 𝑏 is an
  integer greater than 1, and 𝑐, 𝑑 are real numbers with 𝑐 positive and 𝑑 nonnegative. Then
                                     𝑂 𝑛𝑑 ,            if 𝑎 < 𝑏 𝑑
                                         𝑑                        𝑑
                           𝑓 𝑛 =     𝑂 𝑛 log 𝑛 ,       if 𝑎 = 𝑏
                                     𝑂 𝑛log𝑏 𝑎 ,       if 𝑎 > 𝑏 𝑑
