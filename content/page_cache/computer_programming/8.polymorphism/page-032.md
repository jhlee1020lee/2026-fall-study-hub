---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 32
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Constructor Overriding
• Constructor overriding is not possible.
   • Constructors are not inherited in java.

public class Employee {
  protected double salary;
  Employee() { this.salary = 180; }
}
class Manager extends Employee {
  Manager() { this.salary = 250; }                // okay
}
class Manager extends Employee {
  Employee() { this.salary = 250; }               // not okay
}

                                      Jaemin Yoo (SNU)          32
