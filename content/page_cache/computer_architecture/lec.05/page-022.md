---
course: "computer_architecture"
source_pdf: "lec.05.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.pdf"
generated_at: "2026-09-22T04:08:57Z"
---
                 Store Instructions

Assembly (e.g., load 4-byte word)
 ➟ SW rs2reg offset12 (rs1reg)

Machine encoding




FSM transition semantics
 ➟ if MEM[PC]==SW rs2 offset12 (rs1)
      EA = sign-extend(offset) + GPR[rs1]
      MEM[ translate(EA) ] ← GPR[rs2]
      PC ← PC + 4




                                            22 / 38
