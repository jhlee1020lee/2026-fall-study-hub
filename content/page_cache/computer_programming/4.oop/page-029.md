---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
static Members: Example 1

 class Car {
    static int num = 3;
    static void printNum() {
        System.out.println("The number of cars is " + num);
    }
 }

 System.out.println(Car.num);
 Car.printNum();


                            Jaemin Yoo (SNU)                  29
