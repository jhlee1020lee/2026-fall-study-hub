---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Inheritance Syntax

 class Parent {
    int var = 123;
    void func() { System.out.println("Parent"); }
 }
 class Child extends Parent { }

 Parent parent = new Parent();
 Child child = new Child();
 parent.func();
 child.func();
 System.out.println(parent.var);
 System.out.println(child.var);


                                   Jaemin Yoo (SNU)   15
