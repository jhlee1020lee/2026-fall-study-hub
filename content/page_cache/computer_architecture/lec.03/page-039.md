---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 39
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
        More Conditional Operations

blt rs1, rs2, L1 (branch less than)
  ➟ if (rs1 < rs2) branch to instruction labeled L1

bge rs1, rs2, L1 (branch greater than or equal to)
  ➟ if (rs1 >= rs2) branch to instruction labeled L1

Example
  ➟ if (a > b) a += 1;
      ➟ a in x22, b in x23
       bge x23, x22, Exit // branch if b >= a
       addi x22, x22, 1
     Exit:




                                                       39 / 68
