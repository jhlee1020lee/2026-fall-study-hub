---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 65
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
           Synchronization in RISC-V

Load reserved: lr.d rd, (rs1)
  ➟ Load from address in rs1 to rd
  ➟ Place reservation on memory address


Store conditional: sc.d rd, (rs1), rs2
  ➟ Store from rs2 to address in rs1
  ➟ Succeeds if location not changed since the lr.d
       ➟ Returns 0 in rd
  ➟ Fails if location is changed
       ➟ Returns non-zero value in rd




                                                      65 / 68
