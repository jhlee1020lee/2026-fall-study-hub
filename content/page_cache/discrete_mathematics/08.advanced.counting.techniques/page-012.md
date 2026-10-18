---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
Linear Homogeneous Recurrence Relations of Arbitrary Degree
 • Theorem: Let c1, c2 ,…, ck be real numbers. Suppose that the characteristic equation
   rk – c1rk−1 –⋯ – ck = 0 has k distinct roots r1, r2, …, rk. Then a sequence {an} is a solution of
   the recurrence relation an = c1an−1 + c2an−2 + ….. + ck an−k if and only if
                                       𝑎𝑛 = 𝛼1 𝑟1𝑛 + ⋯ + 𝛼𝑘 𝑟𝑘𝑛
  for n = 0, 1, 2, …, where α1, α2,…, αk are constants.


 • Theorem: Let c1, c2 ,…, ck be real numbers. Suppose that the characteristic equation
   rk – c1rk−1 –⋯ – ck = 0 has t distinct roots r1, r2, …, rt with multiplicities m1, m2, …, mt,
   respectively so that mi ≥ 1 for i = 0, 1, 2, …,t and m1 + m2 + … + mt = k. Then a sequence {an}
   is a solution of the recurrence relation an = c1an−1 + c2an−2 + ….. + ck an−k if and only if
      𝑎𝑛 = 𝛼1,0 + ⋯ + 𝛼1,𝑚1−1 𝑛𝑚1 −1 𝑟1𝑛 + ⋯ + 𝛼𝑡,0 + 𝛼𝑡,1 𝑛 + ⋯ + 𝛼𝑡,𝑚𝑡−1 𝑛𝑚𝑡 −1 𝑟1𝑛
  for n = 0, 1, 2, …, where αi,j are constants for 1≤ i ≤ t and 0≤ j < mi.
