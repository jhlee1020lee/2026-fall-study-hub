---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 51
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Constructor Chaining
• There is an order; instance variable initiation comes after the
  superclass constructor call.

     // Order of execution
     ColoredPoint() { super(); }
     Point() { super(); }
     Object() { }
     x = 1; y = 1;
     int color = 0xFF00FF;

                               Jaemin Yoo (SNU)                     51
