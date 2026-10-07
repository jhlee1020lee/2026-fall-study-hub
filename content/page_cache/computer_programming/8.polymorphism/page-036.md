---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 36
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overloading, Overriding, and Hiding


class RealPoint extends Point {
  float x = 0.0f, y = 0.0f;                                   // hiding
  void move(int dx, int dy) { move((float)dx, (float)dy); }   // overriding
  void move(float dx, float dy) { x += dx; y += dy; }         // overloading
  int getX() { return (int)Math.floor(x); }                   // overriding
  int getY() { return (int)Math.floor(y); }                   // overriding
}




                                  Jaemin Yoo (SNU)                             36
