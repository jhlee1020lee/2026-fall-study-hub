---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 50
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Constructor Chaining
• A class constructor calls its superclass constructor.
• The superclass constructor also calls its superclass constructor.
   • It chains up to the Object class.

  class Point {
     int x, y;
     Point() { x = 1; y = 1; }
  }
  class ColoredPoint extends Point {
     int color = 0;
  }

  ColoredPoint cp = new ColoredPoint();                   // What happen?

                                       Jaemin Yoo (SNU)                     50
