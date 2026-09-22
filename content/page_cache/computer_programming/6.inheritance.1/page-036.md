---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 36
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Hiding Variables
• A child class can declare a variable with the same name.


  class Parent {                             Parent parent = new Parent();
     int var = 123;                          Child child = new Child();
  }                                          System.out.println(parent.var);
                                             System.out.println(child.var);
  class Child {
     int var = 456;                          // 123
  }                                          // 456



                              Jaemin Yoo (SNU)                                 36
