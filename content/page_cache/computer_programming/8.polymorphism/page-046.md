---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 46
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Operator Overloading: & and |
• With integers, & and | operate on individual bits.
• With booleans, they compute logical AND and OR.

   int a = 6;                               // binary 110
   int b = 3;                               // binary 011
   System.out.println(a & b);               // 2 (010)
   System.out.println(a | b);               // 7 (111)

   System.out.println(true & false);        // false
   System.out.println(true | false);        // true


                                Jaemin Yoo (SNU)            46
