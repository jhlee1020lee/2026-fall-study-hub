---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Dynamic Binding: Example 1
 class Parent {
     void print() {
         System.out.println("Parent.print()");
     }
 }

 class Child extends Parent {
     @Override
     void print() {
         System.out.println("Child.print()");
     }
 }

                               Jaemin Yoo (SNU)   6
