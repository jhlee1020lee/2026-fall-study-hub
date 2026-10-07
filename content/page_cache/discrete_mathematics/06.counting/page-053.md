---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 53
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
Quiz
Its solution is
                              𝑇 𝑛 = Θ 𝑛, ,
Substitute 𝑇 𝑛 = 𝑛, into the recursive part:
                          𝑛, = (𝑛/2), + (𝑛/4), .
Now simplify:
                                      ,          ,
                                   1           1
                        𝑛, = 𝑛,         + 𝑛,        .
                                   2           4
Factor out 𝑛, :
                           ,     ,
                                     1 ,     1 ,
                         𝑛 =𝑛            +        .
                                     2       4
We need p:
                               1 ,   1 ,
                                   +     = 1.
                               2     4
