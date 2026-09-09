---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 45
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                Leaf Procedure Example
     RISC-V code:

1 leaf_example:
2      addi sp,sp,-24       Save x18, x19, x20 on stack
3      sd x18,16(sp)
4      sd x19,8(sp)
5      sd x20,0(sp)
6      add x18,x10,x11      x18 = g + h
7      add x19,x12,x1       x19 = i + j
8      sub x20,x18,x19      f = x18 – x19
9      addi x10,x20,0       copy f to return register
10     ld x20,0(sp)         Resore x18, x19, x20 from stack
11     ld x19,8(sp)
12     ld x18,16(sp)
13     addi sp,sp,24
14     jalr x0,0(x1)        Return to caller



                       Okay… arithematic operation…


                                                              45 / 68
