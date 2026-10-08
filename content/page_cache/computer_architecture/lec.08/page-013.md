---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
         RAW Hazard Analysis Example




Instructions IA and IB (where IA comes before IB) have RAW hazard iff

  1. IB (R/I, LW, SW, Bxx or JALR) reads a register
     written by IA (R/I or LW, JAL, or JALR)
  2. dist(IA, IB) ≤ dist(ID, WB) = 3

                  What about WAW and WAR hazard?
                  What about memory data hazard?


                                                                        13 / 51
