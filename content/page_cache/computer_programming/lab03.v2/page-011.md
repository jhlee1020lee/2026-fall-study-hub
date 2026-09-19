---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
   Static Members
   ● A static method cannot directly access a non-static variable.

Class Definition                                  Main Method
class Car {
  float fuel;
  static float totalFuel() {
                                                  Car car1 = new Car();
    return fuel;
  }
}

Output

 java: non-static variable fuel cannot be referenced from a static context




                                                                             11
