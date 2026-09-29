---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 42
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Comparable<T> Example: Strings

 String s1 = "aaaaaa";
 String s2 = "bbbbbb";
 String s3 = "bccccc";
 String s4 = "BBBBBB";

 System.out.println(s1.compareTo(s2)); // -1
 System.out.println(s2.compareTo(s1)); // 1
 System.out.println(s1.compareTo(s1)); // 0

 System.out.println(s2.compareTo(s3)); // -1
 System.out.println(s2.compareTo(s4)); // 32

                               Jaemin Yoo (SNU)   42
