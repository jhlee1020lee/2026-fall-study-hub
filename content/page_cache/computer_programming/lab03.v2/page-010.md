---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
   Static Members
   ● Static variables are shared by all objects of the same class.

Class Definition                                Main Method

class Car {
    static String owner;
                                                Car car1 = new Car("Alice");
    Car(String owner) {
                                                Car car2 = new Car("Bob");
        this.owner = owner;
                                                car1.owner = "Carol";
    }
                                                car2.printOwner();
    static void printOwner() {
                                                Car.owner = "David";
        System.out.println(owner);
                                                Car.printOwner();
    }
}


Output

Carol
                                                                               10
David
