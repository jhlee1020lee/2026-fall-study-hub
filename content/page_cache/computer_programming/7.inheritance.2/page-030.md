---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Interface Syntax: implements

 interface MyInterface {
    void printNum(int i);
 }

 // If MyClass doesn't implement printNum, an error is raised
 class MyClass implements MyInterface {
    public void printNum(int i) { System.out.println(i); }
 }


 MyClass myClass = new MyClass();
 myClass.func(123); // 123


                                    Jaemin Yoo (SNU)            30
