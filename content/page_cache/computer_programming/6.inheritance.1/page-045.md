---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 45
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
super for Variables
• Any members of the superclass can be accessed by super.

  class Parent { int var = 123; }
  class Child extends Parent {
     int var = 456;
     int getParentVar() { return super.var; }
  }

  Parent parent = new Parent();
  Child child = new Child();
  System.out.println(parent.var);
  System.out.println(child.var);
  System.out.println(child.getParentVar());

                                   Jaemin Yoo (SNU)         45
