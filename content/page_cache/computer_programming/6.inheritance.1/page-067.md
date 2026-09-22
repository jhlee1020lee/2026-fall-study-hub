---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 67
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Final Method
• Final method prevents subclasses from overriding.

  class Parent {
     final void method() {   System.out.println("out"); }
  }

  class Child extends Parent {
     @Override
     void method() { super.method(); }
  }

  // java: method() in Child cannot override method() in Parent overridden method is
  final

                                      Jaemin Yoo (SNU)                             67
