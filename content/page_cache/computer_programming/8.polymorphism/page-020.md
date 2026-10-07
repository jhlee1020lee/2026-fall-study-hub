---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 20
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Ambiguous Overloading

 class Point { int x, y; }
 class ColoredPoint extends Point { int color; }
 class Test {
    static void test(ColoredPoint p, Point q) {
        System.out.println("(ColoredPoint, Point)");
    }
    static void test(Point p, ColoredPoint q) {
        System.out.println("(Point, ColoredPoint)");
    }
 }

                            Jaemin Yoo (SNU)           20
