---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 48
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
           Why not very deep pipelines?

5-stage pipeline still has plenty of combinational delay between registers
“Superpipelining” → increase pipelining degree such that even intrinsic
operations (e.g., ALU, RF read/write, memory access) require multiple stages
What’s the problem?
Inst0 : r1 ← r2 + r3
Inst1 : r4 ← r1 + 2




                                                                               48 / 51
