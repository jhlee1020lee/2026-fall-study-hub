---
course: "computer_architecture"
source_pdf: "lec.05.typo.fixed.pdf"
pdf_page: 21
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.typo.fixed.pdf"
generated_at: "2026-09-22T04:09:12Z"
---
                  Load Instructions

Assembly (e.g., load 4-byte word)
 ➟ LW rdreg offset12 (rs1reg)

Machine encoding




FSM transition semantics
 ➟ if MEM[PC]==LW rd offset12 (rs1)
      EA = sign-extend(offset) + GPR[rs1]
      GPR[rd] ← MEM[ translate(EA) ]
      PC ← PC + 4




                                            21 / 38
