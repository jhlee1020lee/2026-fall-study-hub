---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 40
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
               Signed vs. Unsigned
Signed comparison: blt, bge
Unsigned comparison: bltu, bgeu
Example

  ➟ x22 = 11111111111111111111111111111111
  ➟ x23 = 00000000000000000000000000000001
  ➟ x22 < x23 // signed
       ➟ –1 < +1
  ➟ x22 > x23 // unsigned
       ➟ +4, 294, 967, 295 > +1




                                             40 / 68
