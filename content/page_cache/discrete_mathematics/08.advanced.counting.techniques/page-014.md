---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
Solving Linear Nonhomogeneous Recurrence Relations
• Theorem: If {an(p)} is a particular solution of the nonhomogeneous linear recurrence
  relation with constant coefficients an = c1an−1 + c2an−2 + ... + ck an−k + F(n), then every
  solution is of the form {an(p) + an(h)}, where {an(h)} is a solution of the associated
  homogeneous recurrence relation an = c1an−1 + c2an−2 + ... + ck an−k.

• Example: Find all solutions of the recurrence relation an = 3an−1 + 2n. What is the solution
  with a1 = 3?
                                                                                        (ℎ)
  – The associated linear homogeneous equation is 𝑎𝑛 = 3𝑎𝑛−1 . Its solutions are 𝑎𝑛 = 𝛼3𝑛 .
                                                                                𝑝
  – To find a particular solution, we might try a linear function in 𝑛, say 𝑎𝑛 = 𝑐𝑛 + 𝑑 where 𝑐 and 𝑑
                                                                                            3
   are constants. It is easy to check that it is a solution if and only if 𝑐 = −1 and 𝑑 = − .
                                                                                            2
                                                        𝑝       ℎ            3
  – Therefore, all solutions are of the form 𝑎𝑛 = 𝑎𝑛 + 𝑎𝑛 = −𝑛 − + 𝛼3𝑛 . To find the solution
                                                                             2
    with 𝑎1 = 3, let 𝑛 = 1 in the above formula for the general solution. Then 𝛼 = 11/6.
