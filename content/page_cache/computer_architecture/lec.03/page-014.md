---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
          Memory Operand Example

C code:
A[12] = h + A[8];
  ➟ Suppose h in x21, base address of A in x22
  ➟ Suppose the size of each element is 8 byte


Compiled RISC-V code:
  ➟ Index 8 requires offset of 64
      ➟ 8 bytes per doubleword
  ➟ ld x9, 64(x22)
    add x9, x21, x9
    sd x9, 96(x22)




                                                 14 / 68
