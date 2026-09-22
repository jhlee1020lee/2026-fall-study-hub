---
course: "computer_architecture"
source_pdf: "lec.05.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.05.pdf"
generated_at: "2026-09-22T04:08:57Z"
---
       Conditional Branch Instructions

Assembly (e.g., branch if equal)
  ➟ BEQ rs1reg rs2reg immediate12

Machine encoding




FSM transition semantics
  ➟ if MEM[PC]==BEQ rs1 rs2 immediate12
       target = PC + sign-extend(immediate) x 2
       if GPR[rs1]==GPR[rs2] then PC ← target
                              else PC ← PC + 4




                                                  25 / 38
