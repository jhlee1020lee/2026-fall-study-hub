---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 64
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                    Synchronization
Two processors sharing an area of memory
  ➟ P1: writes to memory
  ➟ P2: reads and then writes to memory
  ➟ Data race if P1 and P2 don’t synchronize
       ➟ Result depends of order of accesses

Hardware support required
  ➟ Atomic read/write memory operation
  ➟ No other access to the location allowed between the read and write

Could be a single instruction
  ➟ E.g., atomic swap of register   ↔︎ memory
  ➟ Or an atomic pair of instructions




                                                                         64 / 68
