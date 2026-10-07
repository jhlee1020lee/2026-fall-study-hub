---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 34
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Information Hiding
• Redefine static methods or variables of the superclass.

  class Point { static int x = 2; }
  class Test extends Point {
    static double x = 4.7;
    void printX() {
      System.out.println(x + " " + super.x + " " + ((Point)this).x);
    }
  }


  Test test = new Test(); test.printX();           // 4.7 2 2

                                Jaemin Yoo (SNU)                       34
