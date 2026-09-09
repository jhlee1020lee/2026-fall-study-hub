---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 32
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
static Members: Example 3

 class Car {
   float fuel;
   static float totalFuel() {
     return fuel;
   }
 }

 Car car1 = new Car();                  // causes an error.


                            Jaemin Yoo (SNU)                  32
