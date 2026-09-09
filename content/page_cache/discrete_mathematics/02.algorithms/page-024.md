---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 24
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Greedy Scheduling Algorithm
• Solution: At each step, choose the talks with the earliest ending time among the talks
  compatible with those selected.


       procedure schedule(s1 , s2 , … , sn : start times, e1 , e2 , … , en : end times)
           Sort talks by finish time and reorder so that e1 ≤ e2 ≤ … ≤ en
           S := ∅
           for j := 1 to n
                 if talk j is compatible with S then
                        S := S ∪ { j}
           return S [ S is the set of talks scheduled]
