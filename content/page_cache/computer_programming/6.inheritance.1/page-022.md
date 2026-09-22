---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Check “Is-a” Relationship in Java
• Syntax: <instance> instanceof <Class>
• True iff the class of <instance> inherits from <Class>

  class Parent { }
  class Child extends Parent { }

  Parent p = new Parent();
  Child c = new Child();
  System.out.println(p instanceof Parent);            // true
  System.out.println(p instanceof Child);             // false
  System.out.println(c instanceof Child);             // true
  System.out.println(c instanceof Parent);                    // true

                                   Jaemin Yoo (SNU)                     22
