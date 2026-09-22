---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 53
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Accessing Grandparent’s Members
• Can access grandparent’s members only through the parent.

  class Grandparent {
     public void Print(){ System.out.println("Grand");}
  }
  class Parent extends Grandparent {
     public void Print(){ super.Print(); }
  }
  class Child extends Parent {
     public void Print() {
         super.Print();
         System.out.println("Child");
     }
  }

                                      Jaemin Yoo (SNU)        53
