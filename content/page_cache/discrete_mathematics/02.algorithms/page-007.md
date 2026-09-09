---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 7
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
CLRS Algorithm Style (Fibonacci Example)
Algorithm Fibonacci(n)

if n ≤ 1 then                   Symbol               Meaning
   return n              ←                assignment
                                          less-than-or-equal
                         ≤
f1 ← 0                                    comparison
f2 ← 1                   for i ← a to b   counting loop
                         if ... then      conditional
for i ← 2 to n do        return           output result
  temp ← f1 + f2         Algorithm        algorithm declaration
  f1 ← f2
  f2 ← temp

return f2
