---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 45
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Strassen’s Matrix Multiplication
• Suppose we want to multiply two 2𝑛 × 2𝑛 matrices.
                                    𝐶 =𝐴×𝐵
• Instead of multiplying directly, we split each matrix into four blocks.
                                       A11 A12
                                 𝐴=
                                       A21 A22
                                       𝐵11 𝐵12
                                 𝐵=
                                       𝐵21 𝐵22
• Each block is now a 𝑛 × 𝑛 matrix.
