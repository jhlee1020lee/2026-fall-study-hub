---
course: "computer_architecture"
source_pdf: "lec.02.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf"
generated_at: "2026-09-09T01:11:46Z"
---
                Memory Addressing Modes
            Addressing mode: the way to say where data lives in memory

Absolute:                                      LW rt, 10000 // LW=load word
   ➟ use immediate value as address
   ➟ GPR[rt] = MEM[10000]

Register Indirect:                            LW rt, (rbase)
   ➟ GPR[rt] = MEM[GPR[rbase]]

Displaced or based:                           LW rt, offset(rbase)
   ➟ GRP[rt] = MEM[offset+GPR[rbase]]

Indexed:                                      LW rt, (rbase, rindex)
   ➟ GPR[rt] = MEM[GPR[rbase]+GPR[rindex] ]

Memory Indirect                               LW rt ((rbase))
   ➟ GPR[rt] = MEM[MEM[GPR[rbase]]]

Anything else can you think off…

                                                                              15 / 29
