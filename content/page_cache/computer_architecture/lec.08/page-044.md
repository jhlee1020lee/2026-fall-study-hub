---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 44
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
 Load Delay Slot (Alternative Approach)




Delay slot

  ➟ An instruction slot executed without the effects of a preceding instruction
MIPS R2000 defined the LW delay slot

  ➟ Invalid for I2 (in LW’s delay slot) to ask for LW’s result
  ➟ Any dependence on LW at least distance 2
Delay slot in MIPS R2000

  ➟ Fill with an independent instruction
  ➟ Or, fill with a NOP
WARNING: Microarchitecure exposed to outside.

                                                                                  44 / 51
