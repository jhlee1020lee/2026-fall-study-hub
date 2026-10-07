---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 28
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overriding: Return Type
• Return type must also be the same.

  class Employee { public double getSalary() { return 180; } }

  class Laidoff extends Employee {                 // case 2
    public int getSalary() { return 0; }
  }


  System.out.println("E1 : " + (new Employee()).getSalary() +
                     " , E2 : ” + (new Laidoff()).getSalary());

  java: getSalary() in Laidoff cannot override getSalary() in Employee
    return type int is not compatible with double

                                       Jaemin Yoo (SNU)                  28
