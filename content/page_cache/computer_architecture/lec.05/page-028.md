---
course: "computer_architecture"
source_pdf: "lec.05.pdf"
pdf_page: 28
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.pdf"
generated_at: "2026-09-22T04:08:57Z"
---
Unconditional Jump Instructions (Jump and Link)

   Assembly (e.g., branch if equal)
     ➟ JAL rdreg, immediate20

   Machine encoding




   FSM transition semantics
     ➟ if MEM[PC]==JAL rdreg, immediate20
          GPR[rdreg] = PC+4
           PC ←PC + (immediate20 << 2)




                                                  28 / 38
