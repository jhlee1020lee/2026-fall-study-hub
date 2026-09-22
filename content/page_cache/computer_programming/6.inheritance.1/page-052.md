---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 52
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Accessing Grandparent’s Members
• It is prohibited to directly access grandparent’s members.
  class Grandparent {
     public void Print() { System.out.print("Grand"); }
  }
  class Parent extends Grandparent { }
  class Child extends Parent {
     public void Print() {
         super.super.Print();
         System.out.println("Child");
     }
  }

  Child child = new Child();
  child.Print();

                                         Jaemin Yoo (SNU)      52
