---
course: "system_programming"
source_pdf: "Lab1.Decommenter.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/Lab1.Decommenter.pdf"
generated_at: "2026-10-02T05:08:57Z"
---
Requirements – Error: EOF Before a Comment Is Terminated (8/9)



  Standard Input Stream Standard Output Stream                          Standard Error Stream


       abcdefnghi/*n                abcdefnghisn               Error:slines2:sunterminatedscommentn




  ▪ Include the line number where the comment starts in the error message
  ▪ Return EXIT_FAILURE when an unterminated comment was detected
      • Except for this case, you should return EXIT_SUCCESS in all other cases
      • EXIT_FAILURE and EXIT_SUCCESS are defined as macros in stdlib.h
      • so add #include <stdlib.h> to your C code



                                                        11
