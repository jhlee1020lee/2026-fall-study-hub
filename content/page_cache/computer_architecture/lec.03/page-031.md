---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                        Shift Operations




immed: how many positions to shift
Shift left logical

  ➟ Shift left and fill with 0 bits (e.g., 00012 -> 00102 if immed is 1)
                                              ​          ​




  ➟ slli by i bits multiplies by 2i
Shift right logical

  ➟ Shift right and fill with 0 bits (e.g., 00102 -> 00012 if immed is 1)
                                                  ​          ​




  ➟ srli by i bits divides by 2i (unsigned only)




                                                                            31 / 68
