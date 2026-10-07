---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Signature in Java
• Method name and parameter format determine the signature.
  • The return type is not considered.

 // Different signatures
 int add(int, int);
 int add(int, int, int);
 float add(float, float);

 // Same signature; they cannot coexist.
 int add(int, int);
 double add(int, int);

                                  Jaemin Yoo (SNU)            8
