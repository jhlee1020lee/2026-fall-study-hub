---
course: "computer_architecture"
source_pdf: "lec.05.typo.fixed.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.typo.fixed.pdf"
generated_at: "2026-09-22T04:09:12Z"
---
           R-Type ALU Instructions
Assembly (e.g., register-register signed addition)
 ➟ ADD rdreg rs1reg rs2reg

Machine encoding




FSM transition semantics
 ➟ if MEM[PC] == ADD rd rs1 rs2
      GPR[rd] ← GPR[rs1] + GPR[rs2]
      PC ← PC + 4



                                                     13 / 38
