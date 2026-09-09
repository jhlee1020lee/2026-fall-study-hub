---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 42
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
           Procedure Call Instructions

Procedure call: jump and link
jal x1, ProcedureLabel
  ➟ Puts Address of following instruction (e.g., return address) in x1
  ➟ Jumps to target address (procedureLabel)
       ➟ Q. what’s the required bit-space for representing ProcecureLabel?

Procedure return: jump and link register
jalr x0, 0(x1)
  ➟ Like jal, but jumps to 0 + address in x1
  ➟ Use x0 as rd (x0 cannot be changed)
  ➟ Can also be used for computed jumps
       ➟ e.g., for case/switch statements




                                                                             42 / 68
