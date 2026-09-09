---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 51
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
           Non-Leaf Procedure Example

 C code:

1 int64_t fact (int64_t n) {
2     if (n < 1) return 1;
3     else return n * fact(n - 1);
4 }

 n * fact(n - 1) needs the argument (i.e., n) and the result of fact(n-1)
   ➟ Argument n in x10 when it is called
   ➟ Result in x10 when it returns




                                                                            51 / 68
