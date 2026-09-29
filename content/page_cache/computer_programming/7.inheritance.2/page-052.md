---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 52
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Abstract Class Example

 class Student extends Person {
    Student(String description, String name, int age) {
        super(description, name, age);
    }
    public void work() {
        System.out.println("Study hard");
    }
    public void play() {
        System.out.println("Drink hard");
    }
 }

                                 Jaemin Yoo (SNU)         52
