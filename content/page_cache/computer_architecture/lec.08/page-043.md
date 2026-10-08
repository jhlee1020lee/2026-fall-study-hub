---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
Data Hazard Analysis (with Forwarding)




Even with data-forwarding, RAW dependence on an immediate preceding LW
instruction produces a hazard
Stall = {[(rs1ID == rdEX) && use_rs1(IRID)] ||
        [(rs2ID == rdEX) && use_rs2(IRID)] } && MemReadEX



                                                                         43 / 51
