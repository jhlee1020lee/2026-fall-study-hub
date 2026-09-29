---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 50
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Abstract Class Example
 abstract class Person {
    String description;              // non-static, non-field field
    String name;                     // non-static, non-field field
    private int age;                 // private, non-static, non-field field
    public void printName() {
        System.out.println(description + " " + name);
    }
    public void ageOneYear() {
        age++;
        System.out.printf("%s is now %d years old.\n", name, age);
    }
    abstract void work();            // child classes need to implement this.
    abstract void play();            // child classes need to implement this.
 }

                                     Jaemin Yoo (SNU)                           50
