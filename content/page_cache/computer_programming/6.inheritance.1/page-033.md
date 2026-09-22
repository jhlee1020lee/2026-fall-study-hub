---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
@Override Annotation
  class Parent {
     void printName() { System.out.println("Parent"); }
  }
  class Child extends Parent {
     @Override
     void printName() { System.out.println("Child"); }
  }

  Parent parent = new Parent();
  Child child = new Child();
  parent.printName();
  child.printName();

                              Jaemin Yoo (SNU)            33
