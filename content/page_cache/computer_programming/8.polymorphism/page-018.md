---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Constructor Overloading Rules
• One constructor can call another constructor with this().

  import Math;
  class Point {
     private double x, y;

       Point(float x, float y) { this.x = x; this.y = y; }
       Point(int x, int y) { this((float) x, (float) y); }
       Point() { this(0, 0); }
  };

                               Jaemin Yoo (SNU)               18
