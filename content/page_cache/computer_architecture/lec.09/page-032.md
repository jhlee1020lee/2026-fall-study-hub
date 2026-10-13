---
course: "computer_architecture"
source_pdf: "lec.09.pdf"
pdf_page: 32
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.09.pdf"
generated_at: "2026-10-13T03:36:13Z"
---
Alternative: Branch Delay Slots in MIPS R2000




  PC+4 is already in the pipeline

     ➟ Throwing PC+4 away costs 1 bubble
     ➟ Letting PC+4 finish to the end won’t hurt performance
  R2000 defined branches to have an architectural latency of 1 instruction

     ➟ 1st instruction immediately after a branch is always executed
     ➟ Branch target takes effect on the 2nd instruction
     ➟ If we can find an instruction to fill the delay slot, we get ideal IPC of 1 without branch
      prediction or a pipeline flush logic
     ➟ ~80% of delay slots can be filled automatically by compilers



                                                                                                    32 / 33
