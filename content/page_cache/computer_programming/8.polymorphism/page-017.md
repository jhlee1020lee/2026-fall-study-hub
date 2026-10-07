---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 17
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Constructor Overloading
• Define multiple constructors with different parameter formats.

  import Math;
  class Point {
     private double x, y;
     Point() { this.x = 0; this.y = 0; }
     Point(int x, int y) { this.x = x; this.y = y; }
     Point(float x, float y) { this.x = x; this.y = y; }
     Point(double radius, double theta) {
         this.x = radius * Math.cos(theta);
         this.y = radius * Math.sin(theta);
     }
  };

                                   Jaemin Yoo (SNU)                17
