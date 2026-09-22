---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 38
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Type Casting for Variables
• Variables and static methods can be accessed with type casting.

  class Point { int x = 2; }
  class Test extends Point {
     double x = 4.7;
     void printX() {
         System.out.println(x + " " + super.x + " " + ((Point)this).x);
     }
  }

  Test test = new Test();
  test.printX();

                                Jaemin Yoo (SNU)                          38
