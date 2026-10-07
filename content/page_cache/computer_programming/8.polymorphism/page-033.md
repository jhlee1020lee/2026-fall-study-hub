---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overriding Object Methods
• We can override methods of the Object class.
  class Point2D {
      double x, y;
      Point2D(double x, double y) { this.x = x; this.y = y; }
      public String toString() { return "(" + x + "," + y + ")"; }
      public boolean equals (Object o) {
          if(o instanceof Point2D){
              if(x == ((Point2D)o).x && y ==((Point2D)o).y) return true;
          }
          return false;
      }
 }

                                   Jaemin Yoo (SNU)                        33
