---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 46
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Strassen’s Matrix Multiplication
• Instead of 8 block multiplications, compute:
                         𝑀1 = 𝐴11 + 𝐴22 𝐵11 + 𝐵22
                              𝑀2 = 𝐴21 + 𝐴22 𝐵11
                              𝑀3 = 𝐴11 𝐵12 − 𝐵22
                              𝑀4 = 𝐴22 𝐵21 − 𝐵11
                              𝑀5 = 𝐴11 + 𝐴12 𝐵22
                         𝑀6 = 𝐴21 − 𝐴11 𝐵11 + 𝐵12
                        𝑀7 = 𝐴12 − 𝐴22 𝐵21 + 𝐵22

Each multiplication is between 𝑛 × 𝑛 matrices.
