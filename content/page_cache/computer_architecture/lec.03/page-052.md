---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 52
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
            Non-Leaf Procedure Example

     RISC-V code:

1 fact:
2     addi sp,sp,-16
3       sd x1,8(sp)      // Save return address
4       sd x10,0(sp)     // Save n (x10) on stack
5       addi x5,x10,-1   // x5 = n-1
6       bge x5,x0,L1     // if n-1 >= 0, goto L1
7       addi x10,x0,1    // else, n (x10) = 1
8       addi sp,sp,16    // restore stack
 9     jalr x0,0(x1)   // return
10 L1: addi x10,x10,-1 // x10 = x10-1
11      jal x1,fact      // fact(n-1)
12      addi x6,x10,0    // x6 = x10
13      ld x10,0(sp)     // restore caller’s n
14      ld x1,8(sp)      // restore caller’s return addr
15      addi sp,sp,16    // restore stack
16      mul x10,x10,x6   // n * fact(n-1)
17      jalr x0,0(x1)    // return




                                                           52 / 68
