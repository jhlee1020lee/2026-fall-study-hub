---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 55
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Access Modifiers and Inheritance
• Protected members can be accessed from:
  • The class itself, subclasses of the class, or
  • All other classes in the same package of the class.

  class Shape {
     protected double height, width;
     public void setValues(double height, double width) {
        this.height = height; this.width = width;
     }
  }
  class Rectangle extends Shape {
     public double getArea() { return height * width; }
  }


                                      Jaemin Yoo (SNU)      55
