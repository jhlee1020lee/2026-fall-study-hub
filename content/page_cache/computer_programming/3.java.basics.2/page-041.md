---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 41
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Example: Fencepost
• What does the code below print?



 char[] chars = {'c', 'o', 'm', 'p', 'u', 't', 'e', 'r'};
 for (int i = 0; i < chars.length - 1; i++) {
    System.out.print(chars[i] + ",");
 }
 System.out.println(chars[chars.length - 1]);



                             Jaemin Yoo (SNU)               41
