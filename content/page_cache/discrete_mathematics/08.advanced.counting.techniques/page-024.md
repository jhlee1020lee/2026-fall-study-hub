---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 24
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
 The Number of Onto Functions
• Example: How many onto functions are there from a set with six elements to a set with
  three elements?
  – Suppose that the elements in the codomain are b1, b2, and b3. Let P1, P2, and P3 be the properties
   that b1, b2, and b3 are not in the range of the function, respectively. The function is onto if none of
   the properties P1, P2, and P3 hold.
  – By the inclusion-exclusion principle, the number of onto functions from a set with six elements to a
   set with three elements is
                 N − [N(P1) + N(P2) + N(P3)] + [N(P1P2) + N(P1P3) + N(P2P3)] − N(P1P2P3)


• Theorem: Let m and n be positive integers with m ≥ n. Then there are
                   𝑛                𝑛                                𝑛
            𝑛𝑚 −       𝑛−1 𝑚+           𝑛 − 2 𝑚 − ⋯ + −1 𝑛−1              ⋅ 1𝑚
                   1                 2                             𝑛−1
             onto functions from a set with m elements to a set with n elements.
