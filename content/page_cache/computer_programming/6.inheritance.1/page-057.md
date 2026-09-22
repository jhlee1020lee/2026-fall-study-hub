---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 57
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Public and Protected Inheritance
• Public and protected members can be inherited, overridden or
  hidden from subclasses.
  class Point {
     public int x, y;
     protected int useCount = 0;
     static protected int totalUseCount = 0;
     public void move(int dx, int dy) {
         x += dx; y += dy; useCount++; totalUseCount++;
     }
  }
  class PointBack extends Point {
     public void moveBack(int dx, int dy) {
         x -= dx; y -= dy; useCount++; totalUseCount++;
     }
  }


                                              Jaemin Yoo (SNU)   57
