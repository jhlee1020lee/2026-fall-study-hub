---
course: "computer_architecture"
source_pdf: "lec.07.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.07.pdf"
generated_at: "2026-10-07T01:00:24Z"
---
                            Pipeline Idealism

Motivation: “Increase throughput with little increase in hw cost”
   Repetition of identical operations // Same task!

       ➟ The same operation is repeated on a large number of different inputs
   Repetition of independent operations // Independent sub-task!

       ➟ No ordering dependencies between repeated operations
   Uniformly partitionable sub-operations // Same-length sub-task!

       ➟ Can be evenly divided into uniform-latency sub-operations
       ➟ (that do not share resources)


      Good examples: automobile assembly line, doing laundry …
                 …. maybe instruction pipeline???




                                                                                9 / 55
