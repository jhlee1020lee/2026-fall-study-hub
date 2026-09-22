---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Inheritance of Class Members

 class Point {
    int x, y;
    public void move(int dx, int dy) { x += dx; y += dy; }
 }

 class Point3d extends Point {
    int z;
    public void move(int dx, int dy, int dz) {
        x += dx; y += dy; z += dz;
    }
 }

                               Jaemin Yoo (SNU)              16
