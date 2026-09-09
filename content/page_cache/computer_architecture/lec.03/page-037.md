---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 37
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
          Compiling Loop Statements
    C code:
    while (save[i] == k) i += 1;
     ➟ i in x22, k in x24, address of save in x25


    Compiled RISC-V code:

1 Loop: slli x10, x22, 3    // x10 = i * 8
2       add x10, x10, x25   // x10 = address of save + i * 8
3       ld x9, 0(x10)       // x9 = read a value from save[i]
4       bne x9, x24, Exit   // check if save[i] != k
5       addi x22, x22, 1    // i = i + 1
6       beq x0, x0, Loop    // goto Loop
7 Exit: ...




                                                                37 / 68
