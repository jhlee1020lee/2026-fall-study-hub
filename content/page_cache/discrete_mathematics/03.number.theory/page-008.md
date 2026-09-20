---
course: "discrete_mathematics"
source_pdf: "03.Number.Theory.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf"
generated_at: "2026-09-20T23:38:11Z"
---
Binary Addition
 procedure add(a, b: positive integers)
 {the binary expansions of a and b are (an-1,an-2,…,a0)2 and (bn-1,bn-2,…,b0)2, respectively}
      c := 0
      for j := 0 to n − 1
            d := ⌊(aj + bj + c)/2⌋
            sj := aj + bj + c − 2d
            c := d
      sn := c
      return(s0,s1,…, sn){the binary expansion of the sum is (sn,sn-1,…,s0)2}

• Complexity: 𝑂 𝑛 bit operations
