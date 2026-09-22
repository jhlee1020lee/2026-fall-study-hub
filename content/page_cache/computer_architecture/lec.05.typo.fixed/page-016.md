---
course: "computer_architecture"
source_pdf: "lec.05.typo.fixed.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.typo.fixed.pdf"
generated_at: "2026-09-22T04:09:12Z"
---
           I-Type ALU Instructions
Assembly (e.g., register-immediate signed additions)
 ➟ ADDI rdreg rs1reg immediate12

Machine encoding




FSM transition semantics
 ➟ if MEM[PC] == ADDI rd rs1 immediate
      GPR[rd] ← GPR[rs1] + sign-extend (immediate)
      PC ← PC + 4



                                                       16 / 38
