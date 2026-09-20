---
course: "discrete_mathematics"
source_pdf: "03.Number.Theory.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf"
generated_at: "2026-09-20T23:38:11Z"
---
  Binary Multiplication
 procedure multiply(a, b: positive integers) {the binary expansions
 of a and b are (an-1…a0)2 and (bn−1…b0)2, resp.}
       for j := 0 to n − 1
              if bj = 1 then cj = a shifted j places
              else cj := 0 {co,c1,…, cn-1 are the partial products}
       p := 0
       for j := 0 to n − 1
              p := p + cj
       return p {p is the value of ab}

• Complexity: 𝑂 𝑛2
• There exist better algorithms with different pros and cons
  – In 1960, Anatoly Karatsuba developed the Karatsuba algorithm with complexity 𝑂 𝑛log2 3 .
  – The algorithm with the best computational complexity is a 2019 algorithm of Harvey and Hoeven,
   which requires only O(n log n) operations. This is conjectured to be the best possible algorithm.
