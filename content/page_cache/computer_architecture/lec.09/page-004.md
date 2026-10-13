---
course: "computer_architecture"
source_pdf: "lec.09.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.09.pdf"
generated_at: "2026-10-13T03:36:13Z"
---
     Instruction Ordering/Dependencies


Control Dependence

 ➟ Every instruction uses the PC to determine which instruction to fetch
 ➟ Every instruction determines the next PC value
  (PC+4 for sequential, or target address for branches/jumps)
 ➟ Which instructions to execute depends on previous control flow
  (e.g., branch conditions, jump targets)


  In other words, control dependence is data dependence on the PC




                                                                           4 / 33
