---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 42
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Matrix Multiplication Algorithm
• Let C = AB where C is an m x n matrix that is the product of the m x k matrix A
  and the k x n matrix B.

           procedure matrix multiplication (A,B: matrices)
               for i := 1 to m
                     for j := 1 to n
                           cij := 0
                           for q := 1 to k
                                 cij := cij + aiq bqj
           return C = [cij]
