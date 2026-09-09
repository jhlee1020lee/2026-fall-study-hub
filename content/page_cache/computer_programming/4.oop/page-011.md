---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Accessing and Modifying Attributes
• You can access or modify attributes by using the dot syntax (.):

   class Car {
      int width = 10;
      String color = "red";
   }

   Car car = new Car();
   System.out.println(car.width);
   car.width = 5;
   System.out.println(car.width);

                                Jaemin Yoo (SNU)                     11
