---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 42
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
                  Forwarding Logic


if (rs1ID!=0) && (rs1ID==rdEX) && RegWriteEX then

  ➟ forward writeback value from EX // dist=1
else if (rs1ID!=0) && (rs1ID==rdMEM) && RegWriteMEM then

  ➟ forward writeback value from MEM // dist=2
else if (rs1ID!=0) && (rs1ID==rdWB) && RegWriteWB then

  ➟ forward writeback value from WB // dist=3


 Ordering matters!! Must check the youngest match first!




                                                           42 / 51
