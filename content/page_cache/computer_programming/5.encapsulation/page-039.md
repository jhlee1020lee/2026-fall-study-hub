---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 39
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Inner Class: Example

 public class Calculator {
    Adder adder;
    Multiplier multiplier;
    int battery;
    int price;

     Calculator(int battery) { ... }
     int specialOp(int opd1, int opd2) { ... }
     private class Adder { ... }
     private class Multiplier { ... }
 }

                                Jaemin Yoo (SNU)   39
