---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 35
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overloading, Overriding, and Hiding

 class Point {
   int x = 0, y = 0;
   int color;
   int getX() { return x; }
   int getY() { return y; }

     void move(int dx, int dy) { x += dx; y += dy; }
     static void show(int x, int y) {
       System.out.println("(" + x + ", " + y + ")");
     }
     static void show(float x, float y) {
       System.out.println("(" + x + ", " + y + ")");
     }
 }


                                       Jaemin Yoo (SNU)   35
