---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 51
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Abstract Class Example

 class BusinessMan extends Person {
    BusinessMan(String description, String name, int age) {
        super(description, name, age);
    }
    public void work() {
        System.out.println("Meeting all day");
    }
    public void play() {
        System.out.println("Go to the movies");
    }
 }

                                 Jaemin Yoo (SNU)             51
