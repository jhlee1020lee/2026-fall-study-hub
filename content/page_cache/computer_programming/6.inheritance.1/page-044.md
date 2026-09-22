---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 44
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Downcasting

 class Parent {
    void print() { System.out.println("Parent"); }
 }
 class Sister extends Parent {
    void print() { System.out.println("Sister");}
 }
 class Brother extends Parent {
    void print() { System.out.println("Brother"); }
 }

 Parent parent = (Parent) (new Sister());
 parent.print();                                        // Sister
 Sister sister = (Sister) parent;                       // Okay
 Brother sister = (Brother) parent;                     // Not okay


                                     Jaemin Yoo (SNU)                 44
