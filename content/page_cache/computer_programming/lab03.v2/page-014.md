---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
 Memory States
  ● Call-by-Reference
    ● A way to call a function by passing a variable reference pointing to the variable’s
            memory space
       ●    Passing an object is done by Call-by-Reference

Class Definition
                                                                Output
    class Car {
        int speed = 50;                                         100
    }


Main Function
    static void changeSpeed(Car car) {
        car.speed = 100;
    }

    public static void main(String[] args) {
        Car car1 = new Car();
        changeSpeed(car1);
        System.out.println(car1.speed);                                                     14
    }
