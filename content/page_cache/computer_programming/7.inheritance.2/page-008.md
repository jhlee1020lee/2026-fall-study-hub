---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Dynamic Binding: Example 2
 class Shape {
    void draw() { }
    public static Shape randShape() {
        switch ((int)(Math.random() * 2)) {
            default:
            case 0: return new Circle();
            case 1: return new Square();
        }
    }
 }
 class Circle extends Shape {
    void draw() { System.out.println("Circle.draw()"); }
 }
 class Square extends Shape {
    void draw() { System.out.println("Square.draw()"); }
 }


                                          Jaemin Yoo (SNU)   8
