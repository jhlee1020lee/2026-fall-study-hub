---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 41
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                       Procedure Calling

Requirements for procedure (function) calling
   ➟ Passing function parameters
   ➟ Storage to store local variables
   ➟ Pass result
   ➟ Return to caller
In RISC-V, steps required
   1. Place parameters in registers x10 to x17
   2. Transfer control to procedure
   3. Acquire storage for procedure
   4. Perform procedure’s operations
   5. Place result in register for caller
   6. Return to place of call (address in x1)




                                                 41 / 68
