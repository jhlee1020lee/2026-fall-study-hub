---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
      2s-Complement Signed Integers

Given an n-bit number

  ➟ x = −xn−1 ⋅ 2n−1 + xn−2 ⋅ 2n−2 + ⋯ + x1 ⋅ 21 + x0 ⋅ 20
                 ​                ​                    ​




  ➟ Range: -2^{n-1} to +2^{n-1}-1


Example

  ➟ 11111111...111111002      ​




    = –1 × 231 + 1 × 230 + ... + 1 × 22 + 0 × 21 + 0 × 20
    = –2, 147, 483, 648 + 2, 147, 483, 644 = –410​




Using 64 bits: −9,223,372,036,854,775,808
                  to 9,223,372,036,854,775,807



                                                             18 / 68
