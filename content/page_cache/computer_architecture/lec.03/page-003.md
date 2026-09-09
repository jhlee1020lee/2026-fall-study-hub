---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 3
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                              Recap

(Instruction Set) Architecture = programmer visible state
What is “programmer visible state?” (often called “architectural state”)
  ➟ Who is “programmer” in this context?
  ➟ Useful thinkikng:
       ➟ Writing a compiler. What should we know?
            ➟ C code → ?
       ➟ Writing an OS for context switching. What should we know?
            ➟ context-out: a program running in CPU → ?
            ➟ context-in: ? → an empty CPU
       ➟ In all cases, the architectural state is the contract that
        defines how software and hardware interact.




                                                                           3 / 68
