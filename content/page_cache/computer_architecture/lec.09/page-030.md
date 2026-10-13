---
course: "computer_architecture"
source_pdf: "lec.09.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.09.pdf"
generated_at: "2026-10-13T03:36:13Z"
---
 Performance Impact (PC+4 prediction)

Correct guess → No penalty (~86% of the time)
Incorrect guess → 2 bubbles
Assume

  ➟ No data hazards
  ➟ 20% control flow instructions
  ➟ 70% of control flow instructions are taken
IPC = 1 / [ 1 + PRwrong * Penaltywrong ] = 1 / 1.28 = 0.78

  ➟ where PRwrong (Probability of a wrong guess) = 0.2 * 0.7 = 0.14
             Penaltywrong (Penalty for a wrong guess) = 2


          Can we reduce the two penalty terms?



                                                                      30 / 33
