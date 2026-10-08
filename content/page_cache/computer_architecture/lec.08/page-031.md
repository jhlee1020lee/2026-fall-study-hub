---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
                       Stall Condition
Helper functions

  ➟ use_rs1(I) returns true if I uses rs1 && rs1!=x0

Stall when

  ➟ (rs1ID == rdEX) && use_rs1(IRID) && RegWriteEX or

  ➟ (rs1ID == rdMEM) && use_rs1(IRID) && RegWriteMEM or

  ➟ (rs1ID == rdWB) && use_rs1(IRID) && RegWriteWB or

  ➟ (rs2ID == rdEX) && use_rs2(IRID) && RegWriteEX or

  ➟ (rs2ID == rdMEM) && use_rs2(IRID) && RegWriteMEM or

  ➟ (rs2ID == rdWB) && use_rs2(IRID) && RegWriteWB


It is crucial that the EX, MEM and WB stages continue to advance as
                     normal during these stall cycles

                                                                      31 / 51
