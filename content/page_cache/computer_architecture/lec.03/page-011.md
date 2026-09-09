---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
       Register Operand Example


C code:
f = (g + h) - (i + j);
 ➟ Suppose f, …, j in x19, x20, …, x23


Compiled RISC-V code:
add x5, x20, x21
add x6, x22, x23
sub x19, x5, x6




                                         11 / 68
