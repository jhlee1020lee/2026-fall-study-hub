---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 49
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Superclass Constructor Call
• In fact, the superclass’s default constructor is implicitly invoked.
   • Even without explicit superclass constructor call with super().

class Geometry {
   private int dimension;
   Geometry(int dimension) {
      this.dimension = dimension;
   }
   Geometry() { dimension = 3; }
}

class Point extends Geometry{
   Point() {}                       // Same as Point() { super(); }
}

                                    Jaemin Yoo (SNU)                     49
