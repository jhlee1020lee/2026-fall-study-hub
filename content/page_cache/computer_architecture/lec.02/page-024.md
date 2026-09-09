---
course: "computer_architecture"
source_pdf: "lec.02.pdf"
pdf_page: 24
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf"
generated_at: "2026-09-09T01:11:46Z"
---
The ISA Gives Meaning to the Loaded Program

               Assume: PC = 0x1000, GPR[x10] = 0x2000, MEM[0x2000] = 41


 Instructions in .text                        ISA-defined state transitions

  0x1000: lw       x5, 0(x10)                 1. lw   GPR[x5] ← 41
  0x1004: addi x5, x5, 1                      2. addi GPR[x5]   ← 42
  0x1008: sw       x5, 0(x10)                 3. sw   MEM[0x2000] ← 42

                                              PC ← PC + 4 after each instruction




 The loader prepares the memory image; the ISA defines how instructions transform state.




                                                                                           24 / 29
