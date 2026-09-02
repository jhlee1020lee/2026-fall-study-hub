---
course: "discrete_mathematics"
source_pdf: "01.Vectors.and.Matrices.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/01.Vectors.and.Matrices.pdf"
generated_at: "2026-09-02T02:33:41Z"
---
Matrix Multiplication
• Definition: Let 𝑨 be an m × k matrix and 𝑩 be a k × n matrix. The product of 𝑨 and 𝑩,
  denoted by 𝑨𝑩, is the m × n matrix that has its 𝑖, 𝑗 -th element equal to the sum of
  the products of the corresponding elements from the 𝑖-th row of 𝑨 and the 𝑗-th
  column of 𝑩. In other words, 𝑨𝑩 = 𝑐𝑖𝑗 where 𝑐𝑖𝑗 = 𝑎𝑖1 𝑏1𝑗 + 𝑎𝑖2 𝑏2𝑗 + ⋯ + 𝑎𝑖𝑘 𝑏𝑘𝑗 .

             𝑎11    𝑎12   ⋯ 𝑎1𝑘   𝑏11        ⋯ 𝑏1𝑗     ⋯ 𝑏1𝑛
              ⋮      ⋮    ⋱  ⋮                                 ⋱
                                  𝑏21        ⋯ 𝑏2𝑗     ⋯ 𝑏2𝑛
             𝑎𝑖1    𝑎𝑖2   ⋯ 𝑎𝑖𝑘 ⋅                            = ⋯   𝑐𝑖𝑗   ⋯
              ⋮      ⋮    ⋱  ⋮     ⋮         ⋱  ⋮      ⋱  ⋮
                                                                         ⋱
             𝑎𝑚1    𝑎𝑚2   ⋯ 𝑎𝑚𝑘 𝑏𝑘1          ⋯ 𝑏𝑘𝑗     ⋯ 𝑏𝑘𝑛


  – The matrix multiplication is not commutative in general
