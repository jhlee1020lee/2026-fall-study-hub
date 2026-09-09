---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Programming-Style (Fibonacci Example)
function Fibonacci(n):

  if n <= 1:                   Symbol             Meaning
     return n            =              assignment
                         ==             equality comparison
  f1 = 0                                less-than-or-equal
                         <=
  f2 = 1                                comparison
                         :              start of block
  for i from 2 to n:     return         output value
    temp = f1 + f2       function       function declaration
    f1 = f2
    f2 = temp

  return f2
