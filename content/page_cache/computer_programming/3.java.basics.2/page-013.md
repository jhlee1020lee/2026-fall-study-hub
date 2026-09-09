---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Changing a Value in 2D-Array
• Similarly, you can specify two indexes to change an element.
• The below example accesses the 1st array’s 2nd element.



  int[][] myNumbers = {{1, 2}, {3, 4, 5}};
  System.out.println(myNumbers[0][1]); // 2
  myNumbers[0][1] = 0;
  System.out.println(myNumbers[0][1]); // 0


                              Jaemin Yoo (SNU)                   13
