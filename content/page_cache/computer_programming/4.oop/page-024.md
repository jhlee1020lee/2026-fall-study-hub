---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 24
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Accessing Attributes with this

 class Car {
    String color;
    void changeColor() {
        this.color = "red";
        System.out.println(this.color);
        color = "blue";
        System.out.println(color);
    }
 }

 Car car = new Car();
 car.changeColor();


                                  Jaemin Yoo (SNU)   24
