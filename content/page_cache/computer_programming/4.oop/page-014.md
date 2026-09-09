---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Multiple Objects
• Each object has its own attribute values.
• Changing the attribute values of an object does not affect the
  attribute values of other objects.

  Car car = new Car(), newCar = new Car();

  System.out.println(car.color);
  System.out.println(newCar.color);
  newCar.color = "blue";
  System.out.println(car.color);
  System.out.println(newCar.color);

                                Jaemin Yoo (SNU)                   14
