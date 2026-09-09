---
course: "computer_architecture"
source_pdf: "lec.03.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.03.pdf"
generated_at: "2026-09-09T01:11:56Z"
---
             Leaf Procedure Example

 C code:

1 int64_t leaf_example (int64_t g, int64_t h, int64_t i, int64_t j) {
2     int64_t f;
3     f = (g + h) - (i + j);
4     return f;
5 }

 Arguments g, …, j in x10, …, x13
 f in x20
 Temporary registers x18, x19
 Need to save x18, x19, x20 on stack




                                                                        43 / 68
