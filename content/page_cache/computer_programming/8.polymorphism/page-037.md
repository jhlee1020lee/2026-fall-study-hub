---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 37
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overloading, Overriding, and Hiding


RealPoint rp = new RealPoint();
Point p = rp;
rp.move(1.71828f, 4.14159f);                   (0, 0)
p.move(1, -1);                                 (2.7182798, 3.14159)
Point.show(p.x, p.y);                          (2, 3)
Point.show(rp.x, rp.y);                        (2, 3)
Point.show(p.getX(), p.getY());
Point.show(rp.getX(), rp.getY());




                                    Jaemin Yoo (SNU)                  37
