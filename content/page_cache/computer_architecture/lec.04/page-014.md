---
course: "computer_architecture"
source_pdf: "lec.04.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf"
generated_at: "2026-09-14T23:38:17Z"
---
                     Arithmetic Mean
Suppose your workload is applications A0,A1,..An-1

Arithmetic mean of the application run time is

                                   n−1
                             1
                               ∑ TimeAi
                               ​         ​       ​




                             n i=0
                                             ​




  ➟ Comparing AM is the same as comparing total run-time
  ➟ Issue: longer applications have greater contribution than shorter
   applications

If AMX/AMY=n, then Y is n times faster than X
True: A0,…An-1 are run equal number of times always
False: if some applications are run much more frequently then others
(especially problematic if the most frequent applications are also much
shorter than the rest)
                                                                          14 / 23
