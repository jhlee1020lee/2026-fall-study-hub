---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
static Members: Example 2

class Car {
   static int num;               Car car1 = new Car(),
   static int totalMile;             car2 = new Car(),
   int mile;                         car3 = new Car();
   Car() { num++; }              car1.setMile(20);
   void setMile(int mile) {      car2.setMile(30);
       this.mile = mile;         car3.setMile(40);
       totalMile += mile;        System.out.println(Car.num);
   }                             System.out.println(Car.totalMile);
}

                              Jaemin Yoo (SNU)                        30
