---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 61
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
               32-bit Constants

Most constants are small
 ➟ 12-bit immediate is sufficient


For the occasional 32-bit constant
 ➟ lui rd, constant (load upper immediate)
 ➟ Copies 20-bit constant to bits [31:12] of rd
 ➟ Extends bit 31 to bits [63:32]
 ➟ Clears bits [11:0] of rd to 0




                                                  61 / 68
