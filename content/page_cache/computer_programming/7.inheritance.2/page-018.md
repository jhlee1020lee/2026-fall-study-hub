---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
equals() Example
• The String class has already overridden the equals() method.

  String s1 = new String("abc"),
         s2 = new String("abc");
  System.out.println(s1 == s2);
  System.out.println(s1.equals(s2));



  false
  true

                                Jaemin Yoo (SNU)                 18
