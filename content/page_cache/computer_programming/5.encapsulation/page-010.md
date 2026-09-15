---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Access Modifiers: private
• Private attributes are not accessible by other classes.

   class Person {
      private int weight = 80;
   }

   Person jack = new Person();
   System.out.println(jack.weight);

   // java: weight has private access in Person

                                 Jaemin Yoo (SNU)           10
