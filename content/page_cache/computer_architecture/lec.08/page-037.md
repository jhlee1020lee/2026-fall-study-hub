---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 37
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
  Resolving RAW Hazard by Forwarding
Instructions IA and IB (where IA comes before IB) have RAW hazard iff

  ➟ IB (R/I, LW, SW, Bxx or JALR) reads a register
     written by IA (R/I or LW, JAL, or JALR)

  ➟ dist(IA, IB) ≤ dist(ID, WB) = 3
Before: IB needs to stall for RF to update

Now: IB needs to stall for IA to produce result

  ➟ Retrieve IA result from datapath when ready.

  ➟ Must retrieve from youngest if multiple hazards.
       ➟ add ra r- r-
       1.
       ➟ add ra r- r-
       2.
       ➟ add ra r- r-
       3.
       ➟ add r- ra r- (should come from 3.)
       4.


                                                                        37 / 51
