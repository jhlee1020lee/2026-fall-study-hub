---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Overriding Example
 class Point {
    int x = 0, y = 0;
    void move(int dx, int dy) { x += dx; y += dy; }
 }
 class SlowPoint extends Point {
    int xLimit = 10, yLimit = 10;
    void move(int dx, int dy) {
        super.move(limit(dx, xLimit), limit(dy, yLimit));
    }
    static int limit(int d, int limit) {
        return d > limit ? limit : d < -limit ? -limit : d;
    }
 }

                                  Jaemin Yoo (SNU)            31
