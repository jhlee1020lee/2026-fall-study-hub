---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 61
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Private Member Inheritance
• Subclass does not inherit the private members of its parent class.
   • More precisely, it is invisible.

  class Point {
     int x, y;
     void move(int dx, int dy) { x += dx; y += dy; totalMoves++; }
     private static int totalMoves;
  }
  class Point3d extends Point { int z;
     void move(int dx, int dy, int dz) {
         super.move(dx, dy); z += dz;
         totalMoves++; // error
     }
  }

                                        Jaemin Yoo (SNU)             61
