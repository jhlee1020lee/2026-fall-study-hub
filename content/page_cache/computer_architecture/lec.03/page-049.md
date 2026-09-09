---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 49
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
NOTE: Caller and Callee Saved Registers

 Callee-Saved Registers
   ➟ Caller says to callee, “The values of these registers should not
    change when you return to me.”
   ➟ Callee says, “If I need to use these registers, I promise to save the old
    values to memory first and restore them before I return to you.”
    → “hey caller! I am giving you back original values on return.”
 Caller-Saved Registers
   ➟ Caller says to callee, “If there is anything I care about in these
    registers, I already saved it myself.”
   ➟ Callee says to caller, “Don’t count on them staying the same values
    after I am done.”
    → “hey callee! I saved it in my space. use it as you want.”


                                                                                 49 / 68
