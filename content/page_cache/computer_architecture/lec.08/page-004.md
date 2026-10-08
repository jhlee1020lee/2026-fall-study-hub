---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
                  Data Dependence

Data dependence (Read-after-Write (RAW))
r3 ← r1 op r2
r5 ← r3 op r4

Anti-dependence (Write-after-Read (WAR))
r3 ← r1 op r2
r1 ← r4 op r5

Output-dependence (Write-after-Write (WAW))
r3 ← r1 op r2
r5 ← r3 op r4
r3 ← r6 op r7




                                              4 / 51
