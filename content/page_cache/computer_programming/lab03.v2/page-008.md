---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
  Constructors
      ● Special class methods for initializing objects
        ● Called once when the instance is created
        ● Named the same as the class
        ● Does not have a return type
        ● Cannot be called explicitly
        ● Can be given multiple parameters to initialize attributes
        ● Can define multiple constructors with different parameters
Class Definition                                                       Main Function
                                                                        Car myCar = new Car(1234, "Sonata");
  class Car {
                                                                        System.out.println(myCar.carNumber + " " + mayCar.model);
      int carNumber;
      String model;
                                                                       Main Function Output
       Car(int carNumber, String model) {
           this.carNumber = carNumber;                                  Car initialized.
           this.model = model;                                          1234 Sonata
                             System.out.println("Car initialized.");
       }
  }
                                                                                                                                8
