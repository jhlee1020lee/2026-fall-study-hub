---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 35
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Invocation of Hidden Static Methods

 class Super {
    static String greeting() { return "Goodnight"; }
    String name() { return "Richard"; }
 }
 class Sub extends Super {
    static String greeting() { return "Hello"; }
    String name() { return "Henry"; }
 }

 Super s = new Sub();
 System.out.println(s.greeting() + ", " + s.name());

                             Jaemin Yoo (SNU)          35
