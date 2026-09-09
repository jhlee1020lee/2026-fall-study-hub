---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Methods and Attribute Values
• Attribute values used by a method differ between objects.
  • Since each object has its own attribute values.


  class Car {                   Car myCar = new Car();
     int speed;                 Car yourCar = new Car();

                                myCar.speed = 100;
      int getSpeed() {
                                yourCar.speed = 90;
          return speed;
      }                         System.out.println(myCar.getSpeed());
  }                             System.out.println(yourCar.getSpeed());

                                  Jaemin Yoo (SNU)                        16
