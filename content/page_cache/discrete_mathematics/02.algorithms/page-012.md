---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Binary Search - pseudocode

 procedure binary search(x: integer, a1,a2,…, an: increasing integers)
     i := 1 {i is the left endpoint of interval}
     j := n {j is right endpoint of interval}
     while (i < j)
           m := ⌊(i + j)/2⌋
           if x > am then i := m + 1
           else j := m
     if x = ai then location := i
     else location := 0
     return location
