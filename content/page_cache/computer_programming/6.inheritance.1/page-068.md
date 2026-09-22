---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 68
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Final Variables
• The value of the final attribute can never be changed.

  class Point {
     int x, y; int useCount;
     Point(int x, int y) { this.x = x; this.y = y; }
     static final Point origin = new Point(0, 0);
  }

  Point p = new Point(0, 0);
  p.origin = new Point(-1,-2);      // error


  // Note that the state of p can be changed; e.g., its x, y, or useCount.

                                     Jaemin Yoo (SNU)                        68
