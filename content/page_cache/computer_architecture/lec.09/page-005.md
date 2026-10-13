---
course: "computer_architecture"
source_pdf: "lec.09.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.09.pdf"
generated_at: "2026-10-13T03:36:13Z"
---
               “PC” Data Hazard Analysis




THe distance between stages is at least 1

   ➟ Recall: a hazard iff dist(insti, instj) ≤ dist(StageX, StageY)
Does that mean we must stall after every instruction? (for consecutive instructions)

   ➟ IF stage can’t know which PC to fetch next until the current PC is fetched and
    decoded

                                                                                       5 / 33
