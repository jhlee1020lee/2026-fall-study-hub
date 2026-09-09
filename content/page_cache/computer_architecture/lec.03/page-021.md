---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 21
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                      Sign Extension

Representing a number using more bits
  ➟ Preserve the numeric value

Replicate the sign bit to the left
  ➟ c.f. unsigned values: extend with 0s

Examples: 8-bit to 16-bit
  ➟ +2: 0000 0010 => 0000 0000 0000 0010
  ➟ –2: 1111 1110 => 1111 1111 1111 1110

In RISC-V instruction set
  ➟ lb: sign-extend loaded byte
  ➟ lbu: zero-extend loaded byte


                                           21 / 68
