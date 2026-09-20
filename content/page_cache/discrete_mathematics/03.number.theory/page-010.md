---
course: "discrete_mathematics"
source_pdf: "03.Number.Theory.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf"
generated_at: "2026-09-20T23:38:11Z"
---
Modular Exponentiation
• In cryptography, it is important to be able to find bn mod m efficiently, where b, n, and m are
  large integers.
  – It is often impractical to first compute bn and then compute bn mod m.
  – Idea: Use the binary expansion of n.

        procedure modular exponentiation(b: integer, n = (ak-1…a0)2, m: positive integer)
            x := 1
            power := b mod m
            for i := 0 to k − 1
                  if ai= 1 then x := (x∙ power ) mod m
                  power := (power∙ power) mod m
            return x {x equals bn mod m }
