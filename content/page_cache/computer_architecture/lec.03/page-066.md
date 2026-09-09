---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 66
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
            Synchronization in RISC-V

 Example 1: atomic swap (to test/set lock variable)

1 again:    lr.d x10,(x20)
2           sc.d x11,(x20),x23 // X11 = status
3           bne x11,x0,again   // branch if store failed
4           addi x23,x10,0     // X23 = loaded value

 Example 2: lock

1           addi x12,x0,1      // copy locked value
2 again:    lr.d x10,(x20)     // read lock
3           bne x10,x0,again   // check if it is 0 yet
4           sc.d x11,(x20),x12 // attempt to store
5           bne x11,x0,again   // branch if fails
6 Unlock:
7           sd x0,0(x20)       // free lock




                                                           66 / 68
