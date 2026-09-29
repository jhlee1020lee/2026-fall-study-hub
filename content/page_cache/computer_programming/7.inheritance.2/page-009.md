---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Dynamic Binding: Example 2

 Shape[] shapes = new Shape[4];
 for (int i = 0; i < shapes.length; i++)
    shapes[i] = Shape.randShape();
 for (int i = 0; i < shapes.length; i++)
    shapes[i].draw();

 Circle.draw()
 Square.draw()
 Circle.draw()
 Circle.draw()

                               Jaemin Yoo (SNU)   9
