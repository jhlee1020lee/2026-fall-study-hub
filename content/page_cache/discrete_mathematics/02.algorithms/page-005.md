---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Finding the Maximum Element in a Finite Sequence
• The algorithm in pseudocode:


             procedure max(a1, a2, …., an: integers)
                max := a1
                for (i := 2 to n)
                     if max < ai then max := ai
                return max         // max is the largest element
