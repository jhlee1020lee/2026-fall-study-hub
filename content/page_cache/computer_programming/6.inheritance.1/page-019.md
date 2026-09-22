---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Circle-Ellipse Problem
• Circle is an Ellipse, but it may be inappropriate to inherit from it.
   • Since a Circle can lose its characteristic as a circle if stretched.

  class Ellipse{
     float axisX, axisY;
     Ellipse(float x, float y){axisX = x; axisY = y;}
     public void stretchX(float scaleX){ axisX *= scaleX; }
     public void stretchY(float scaleY){ axisY *= scaleY; }
  }
  class Circle extends Ellipse{
     Circle(float radius){
         super(radius,radius);
     }
  }

                                      Jaemin Yoo (SNU)                      19
