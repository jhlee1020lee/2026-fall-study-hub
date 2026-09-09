---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 59
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                   String Copy Example
    RISC-V code:

1 strcpy:
2     addi sp,sp,-8     // adjust stack for 1 doubleword
3       sd x19,0(sp)    // push x19
4       add x19,x0,x0   // i=0
5 L1: add x5,x19,x11    // x5 = addr of y[i]
6     lbu x6,0(x5)      // x6 = y[i]
7     add x7,x19,x10    // x7 = addr of x[i]
8       sb x6,0(x7)     // x[i] = y[i]
9       beq x6,x0,L2    // if y[i] == 0 then exit
10     addi x19,x19,1   // i = i + 1
11     jal x0,L1        // next iteration of loop
12 L2: ld x19,0(sp)     // restore saved x19
13     addi sp,sp,8     // pop 1 doubleword from stack
14 jalr x0,0(x1)        // and return




                                                           59 / 68
