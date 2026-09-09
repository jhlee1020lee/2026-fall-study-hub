---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 47
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Strassen’s Matrix Multiplication
                        𝐶11 = 𝑀1 + 𝑀4 − 𝑀5 + 𝑀7
                             𝐶12 = 𝑀3 + 𝑀5
                             𝐶21 = 𝑀2 + 𝑀4
                        𝐶22 = 𝑀1 − 𝑀2 + 𝑀3 + 𝑀6
• Then combine the blocks:
                                  𝐶11 𝐶12
                             𝐶=
                                  𝐶21 𝐶22

• Instead of 8 multiplications, we only perform 7 multiplications

• Using the Master Theorem
                               𝑇 𝑛 = 𝑂 n2.81
