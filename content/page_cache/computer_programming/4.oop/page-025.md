---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Calling Methods with this

 class Car {
    int speed = 100;
    String speedAndUnit() {
        return speed + " km/h";
    }
    void printSpeedAndUnit() {
        System.out.println(this.speedAndUnit());     // can be omitted.
    }
 }

 Car car = new Car();
 car.printSpeedAndUnit();


                                  Jaemin Yoo (SNU)                        25
