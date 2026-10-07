---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 26
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overriding

 class Employee {
    public double getSalary() { return 180; }
 }
 class Manager extends Employee {
    @Override
    public double getSalary() { return 250; }
 }


 Employee e = new Employee();
 Manager m = new Manager();
 System.out.println("Employee : " + e.getSalary() + ", Manager : ” + m.getSalary());

 // Employee : 180.0, Manager : 250.0


                                        Jaemin Yoo (SNU)                               26
