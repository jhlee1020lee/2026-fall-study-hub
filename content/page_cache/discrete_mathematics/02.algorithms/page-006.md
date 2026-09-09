---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Rosen style (Fibonacci Example)
procedure fibonacci(n : integer)

if n ≤ 1 then
   return n                               Symbol                 Meaning
                                   :=                  assignment
                                   :                   type specification
f1 := 0
                                                       less-than-or-equal
f2 := 1                            ≤
                                                       comparison
                                   for (i := a to b)   counting loop
for (i := 2 to n)                  if ... then         conditional statement
  temp := f1 + f2                  return              output result
  f1 := f2                         procedure           algorithm declaration
  f2 := temp

return f2
