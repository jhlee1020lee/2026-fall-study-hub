---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 57
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
     Byte/Halfword/Word Operations

RISC-V byte/halfword/word load/store
  ➟ Load byte/halfword/word: Sign extend to 64 bits in rd
       ➟ lb rd, offset(rs1)
       ➟ lh rd, offset(rs1)
       ➟ lw rd, offset(rs1)
  ➟ Load byte/halfword/word unsigned: Zero extend to 64 bits in rd
       ➟ lbu rd, offset(rs1)
       ➟ lhu rd, offset(rs1)
       ➟ lwu rd, offset(rs1)
  ➟ Store byte/halfword/word: Store rightmost 8/16/32 bits
       ➟ sb rs2, offset(rs1)
       ➟ sh rs2, offset(rs1)
       ➟ sw rs2, offset(rs1)



                                                                     57 / 68
