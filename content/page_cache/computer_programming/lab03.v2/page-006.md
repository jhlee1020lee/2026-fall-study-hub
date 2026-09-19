---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
Objects and Classes
● Members
  ● Attributes and methods of a Java class
● Attributes
  ● Properties of an object
       ● i.e. Appearance, State, etc.
● Methods
  ● How objects change its attributes and perform actions
        Class Definition             Main Function
          class Car {
              // Attribute            Car newCar = new Car();
              int speed = 10;         System.out.println(newCar.speed); // 10
              // Method               System.out.println(newCar.getSpeed()); // 100
              int getSpeed() {
                  return 10*speed;
              }
          }

                                                                                      6
