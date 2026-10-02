---
course: "system_programming"
source_pdf: "Lab1.Decommenter.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/Lab1.Decommenter.pdf"
generated_at: "2026-10-02T05:08:57Z"
---
How to Test Your Code

 ▪   “assignment1/reference/” directory
      • Sample executable file (sampledecomment) is located
 ▪   “assignment1 /test_files/” directory
      • Sample test*.c files are located
 ▪   “diff” command: Check differences between two files
 ▪   Here is an example:
      • ./sampledecomment < decomment.c > output1 2> errors1
      • ./decomment < decomment.c > output2 2> errors2
      • diff -c output1 output2
      • diff -c errors1 errors2
      • rm output1 errors1 output2 errors2



                                              14
