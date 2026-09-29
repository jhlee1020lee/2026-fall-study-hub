---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
toString() Example
• + operation with another String automatically casts the object to
  the String class using the overridden toString() method.

  class MyClass {
     @Override
     public String toString() {
         return "MyClass";
     }
  }

  MyClass myClass = new MyClass();
  System.out.println("String = " + myClass);

                                   Jaemin Yoo (SNU)                   14
