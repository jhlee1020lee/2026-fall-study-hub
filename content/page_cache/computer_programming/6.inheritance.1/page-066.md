---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 66
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Final Class
• Final class cannot be inherited.



  class Point { int x, y; }
  final class ColoredPoint extends Point { int color; }
  class Colored3DPoint extends ColoredPoint { int z; }

  // java: cannot inherit from final ColoredPoint



                                Jaemin Yoo (SNU)          66
