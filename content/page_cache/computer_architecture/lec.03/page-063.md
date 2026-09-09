---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 63
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                 Jump Addressing

Jump and link (jal) target uses 20-bit immediate for larger range
UJ format:




For long jumps, e.g., to 32-bit absolute address
  ➟ lui: load address[31:12] to temp register
  ➟ jalr: add address[11:0] and jump to target




                                                                    63 / 68
