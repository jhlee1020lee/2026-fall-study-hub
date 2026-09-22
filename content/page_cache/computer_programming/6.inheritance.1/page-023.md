---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Check “Is-a” Relationship in Java
• To check that all classes are descendants of the class Object.

  class MyClass { }


  MyClass myClass = new MyClass();
  String string = new String();
  Integer integer = 3;
  System.out.println(myClass instanceof MyClass);     // true
  System.out.println(myClass instanceof Object);      // true
  System.out.println(string instanceof Object);       // true
  System.out.println(integer instanceof Object);      // true

                                   Jaemin Yoo (SNU)                23
