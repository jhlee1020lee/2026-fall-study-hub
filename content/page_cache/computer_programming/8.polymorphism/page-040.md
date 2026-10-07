---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 40
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Handling Overloading
• At compile time, Java selects which overloaded method to call
  based on the number and types of the arguments.



   Polynomial poly = new Polynomial(“3*x^2 + 5”);
   poly.times(9);
   poly.times(85.2f);
   poly.times(new Polynomial(“2.95 * x + 22”), 3);



                             Jaemin Yoo (SNU)                     40
