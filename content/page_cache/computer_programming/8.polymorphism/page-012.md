---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Why Overloading?
• Case 1: Handle the same task on different data types.

  class Point {             // supports both argument data types.
     float x, y;
     void move(int dx, int dy) { x += dx; y += dy; }
     void move(float dx, float dy) { x += dx; y += dy; }
     public String toString() { return "("+x+", "+y+")"; }
  }

  Point p = new Point();
  p.move(3, 0);
  p.move(0.0f, 4.0f);


                                   Jaemin Yoo (SNU)                 12
