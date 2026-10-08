---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
                       When to Stall?


Instructions IA and IB (where IA comes before IB) have RAW hazard iff

  ➟ IB (R/I, LW, SW, Bxx or JALR) reads a register
    written by IA (R/I or LW, or JAL, JALR)

  ➟ Dist(IA, IB) ≤ dist(ID, WB) = 3

In other words, we must stall IB in ID stage if it wants to read a register
to be written by ALL IA that might exist in EX, MEM or WB stage




                                                                              30 / 51
