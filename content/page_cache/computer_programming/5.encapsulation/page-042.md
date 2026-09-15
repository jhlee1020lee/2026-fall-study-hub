---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 42
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Inner Class: Example

 private class Adder {                           private class Multiplier {
    int price;                                      int price;

     Adder(int battery) {                               Multiplier(int battery) {
         this.price = 500 * battery;                        this.price = 1000 * battery;
     }                                                  }

     int add(int opd1, int opd2) {                      int multiply(int opd1, int opd2) {
         return opd1 + opd2;                                return opd1 * opd2;
     }                                                  }
 }                                               }


                                     Jaemin Yoo (SNU)                                      42
