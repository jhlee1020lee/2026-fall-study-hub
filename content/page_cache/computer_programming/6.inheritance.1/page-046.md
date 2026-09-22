---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 46
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
super for Methods
 class Parent {
    void printName() { System.out.println("Parent"); }
 }

 class Child extends Parent {
    @Override
    void printName() { System.out.println("Child"); }
    void printParentName() { super.printName(); }
 }

 Child child = new Child();
 child.printName();
 child.printParentName();

                                  Jaemin Yoo (SNU)       46
