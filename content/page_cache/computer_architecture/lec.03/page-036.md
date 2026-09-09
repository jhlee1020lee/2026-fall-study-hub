---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 36
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                 Compiling If Statements

   C code:

if (i==j) f = g+h;
else f = g-h;

   f, g, … in x19, x20, …

   Compiled RISC-V code:

      bne x22, x23, Else
      add x19, x20, x21
      beq x0,x0,Exit // unconditional
Else: sub x19, x20, x21
Exit: ...




                                           36 / 68
