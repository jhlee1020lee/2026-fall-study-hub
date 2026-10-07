---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 27
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overriding: Return Type
• Return type must also be the same.

  class Employee { public double getSalary() { return 180; } }

  class Laidoff extends Employee {                 // case 1
    public double getSalary() { return 0; }
  }

  class Laidoff extends Employee {                 // case 2
    public int getSalary() { return 0; }
  }

                                Jaemin Yoo (SNU)                 27
