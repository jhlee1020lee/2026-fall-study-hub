---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overloading
• Methods can have the same name with different signatures.
• Which function to call is determined by parameter types.


  class Point {
     float x, y;
     void move(int dx, int dy) { x += dx; y += dy; }
     void move(float dx, float dy) { x += dx; y += dy; }
     public String toString() { return "("+x+", "+y+")"; }
  }


                             Jaemin Yoo (SNU)                 11
