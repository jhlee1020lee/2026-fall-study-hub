---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 21
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
equals() Example
 Shoes s1 = new Shoes("Nice", "AirMax", 265),
       s2 = new Shoes("Nice", "AirMax", 265),
       s3 = s1;
 System.out.println(s1 == s2);
 System.out.println(s1.equals(s2));
 System.out.println(s1 == s3);
 System.out.println(s1.equals(s3));


 false
 true
 true
 true

                                  Jaemin Yoo (SNU)   21
