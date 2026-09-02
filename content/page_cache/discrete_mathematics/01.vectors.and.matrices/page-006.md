---
course: "discrete_mathematics"
source_pdf: "01.Vectors.and.Matrices.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/01.Vectors.and.Matrices.pdf"
generated_at: "2026-09-02T02:33:41Z"
---
Matrix Arithmetic in ML
• Matrix multiplication is used to compute the weighted sum of inputs in a
  neural network. Matrix addition often appears when adding a bias term to a
  batch of outputs.
                                               2
• Example: Input features of one sample: 𝑋 =     ,
                                               3
                                   1 4                    2
             weight matrix: 𝑊 =         , bias matrix 𝐵 =
                                   2 5                    1

• Interpretation in ML:
                               1      4 2   2   16
                      𝑊𝑋 + 𝐵 =            +   =
                               2      5 3   1   20

• This is exactly what happens in a neural network layer
