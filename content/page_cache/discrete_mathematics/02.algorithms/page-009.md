---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Searching Problems
• Def: The general searching problem is to locate an element 𝑥 in the list of
  distinct elements 𝑎1 , … , 𝑎𝑛 , or determine that it is not in the list.
  – The solution to a searching problem is the location of the term in the list that equals 𝑥 (that is, 𝑖
   is the solution if 𝑥 = 𝑎𝑖 ) or 0 if 𝑥 is not in the list.
  – We will study two different searching algorithms: linear search and binary search.

           procedure linear search( x: integer, a1, a2, …,an: distinct integers)
              i := 1
              while (i ≤ n and x ≠ ai) i := i + 1
              if i ≤ n then location := i
              else location := 0
              return location
