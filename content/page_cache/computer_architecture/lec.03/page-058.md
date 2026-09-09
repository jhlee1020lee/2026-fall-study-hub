---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 58
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
                 String Copy Example

    C code:
     ➟ Null-terminated string
1 void strcpy (char x[], char y[])
2 {
3       size_t i;
4       i = 0;
5       while ((x[i]=y[i])!='\0')
6             i += 1;
7 }




                                       58 / 68
