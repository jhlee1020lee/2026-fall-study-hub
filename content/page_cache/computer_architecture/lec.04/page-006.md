---
course: "computer_architecture"
source_pdf: "lec.04.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf"
generated_at: "2026-09-14T23:38:17Z"
---
                     IPC, MIPS and GHz
The metrics you are most likely to see
  ➟ IPC (instruction per cycle) or CPI (cycle per instruction)
  ➟ MIPS (million instruction per second)
  ➟ GHz (109 cycles per second)
Performance measure
  ➟ execution time = (time/cyc) x (cyc/inst) x (inst/program)
       ➟ time/cyc = 1/GHz
       ➟ (time/cyc) x (cyc/inst) = 1/MIPS
  ➟ MIPS and IPC are averages
  ➟ These factors are highly related as design trade-offs
       ➟ GHz ← semiconductor tech & uarch
       ➟ CPI ← uarch & ISA
       ➟ inst/program ← ISA & compiler

                                                                 6 / 23
