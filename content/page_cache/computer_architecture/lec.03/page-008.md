---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                Arithmetic Example


C code:
f = (g + h) - (i + j);


Compiled RISC-V code:
add t0, g, h // temp t0 <- g + h
add t1, i, j // temp t1 <- i + j
sub f, t0, t1 // f <- t0 - t1
(t0, t1, g, h, i, j, f are virtual register names)




                                                     8 / 68
