---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
  Fast Integer Multiplication
• An algorithm for the fast multiplication of two 2n-bit integers (assuming n is even) first splits
  each of the 2n-bit integers into two blocks, each of n bits.
  – Let 𝑎 = 2𝑛 𝑎1 + 𝑎0 and 𝑏 = 2𝑛 𝑏1 + 𝑏0
  – The algorithm is based on the fact that ab can be rewritten as:
                 𝑎𝑏 = 22𝑛 + 2𝑛 𝑎1 𝑏1 − 2𝑛 𝑎1 − 𝑎0 𝑏1 − 𝑏0 + 2𝑛 + 1 𝑎0 𝑏0
  – Hence, if 𝑓 𝑛 is the total number of operations needed to multiply two n-bit integers, then
                                       𝑓 2𝑛 = 3𝑓 𝑛 + 𝐶𝑛
     where 𝐶𝑛 represents the total number of bt operations; the additions, subtractions and shifts
