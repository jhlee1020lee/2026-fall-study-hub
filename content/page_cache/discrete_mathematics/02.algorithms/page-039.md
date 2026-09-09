---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 39
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Worst-Case Complexity of Linear Search
       procedure linear search( x: integer, a1, a2, …,an: distinct integers)
           i := 1
           while (i ≤ n and x ≠ ai) i := i + 1
           if i ≤ n then location := i
           else location := 0
           return location

 • Count the number of comparisons.
   – At each step two comparisons are made; i ≤ n and x ≠ ai .
   – To end the loop, one comparison i ≤ n is made.
   – After the loop, one more i ≤ n comparison is made.

 • If x = ai , 2i + 1 comparisons are used. If x is not on the list, 2n + 1 comparisons are
   made and then an additional comparison is used to exit the loop. So, in the worst case
   2n + 2 comparisons are made. Hence, the complexity is Θ(n).
