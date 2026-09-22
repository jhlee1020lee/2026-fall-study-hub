---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 63
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Private Attribute Inheritance

 class Point {
    private int x, y;
    void move(int dx, int dy) {
        x += dx; y += dy;
    }
 }

 class Point3d extends Point {
    private int z;
    void move(int dx, int dy, int dz) {
        super.move(dx, dy);
        z += dz;
    }
 }


                                     Jaemin Yoo (SNU)   63
