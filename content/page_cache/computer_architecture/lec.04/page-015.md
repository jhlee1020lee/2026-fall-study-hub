---
course: "computer_architecture"
source_pdf: "lec.04.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf"
generated_at: "2026-09-14T23:38:17Z"
---
              Weighted Arithmetic Mean
Introduce weighting factors, w0,w1…wn-1 where

                                                n−1
                                     1 = ∑ wi         ​   ​




                                                i=0

wi is the number of times Ai runs relative to total number of times any program in the
workload is run
Weighted arithmetic mean of the run time is

                                  n−1
                                  ∑ wi ⋅ TimeAi
                                        ​   ​


                                                              ​
                                                                  ​




                                  i=0

If WAMX/WAMY=n then Y is n times faster than X on a workload characterized by
w0,w1…wn-1


      Yes, you get a number at the end, but what does it mean?


                                                                                         15 / 23
