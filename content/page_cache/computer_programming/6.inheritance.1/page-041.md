---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 41
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Upcasting
• Both intrinsic casting and explicit casting are available.


  class Parent { }
  class Child extends Parent { }



  Parent parent1 = new Child(); // Intrinsic Casting
  Parent parent2 = (Parent) (new Child()); // Explicit Casting


                              Jaemin Yoo (SNU)                   41
