---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 40
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Inner Class: Example


 Calculator(int battery) {
    this.battery = battery;
    this.adder = new Adder(battery);
    this.multiplier = new Multiplier(battery);
    this.price = this.adder.price + this.multiplier.price;
 }




                            Jaemin Yoo (SNU)                 40
