---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Loop Through a 2D Array
• We can also use a nested for loop to iterate a 2D array.



 int[][] myNumbers = {{1, 2, 3}, {4, 5}};
 for (int i = 0; i < myNumbers.length; ++i) {
    for (int j = 0; j < myNumbers[i].length; ++j) {
        System.out.println(myNumbers[i][j]);
    }
 }

                               Jaemin Yoo (SNU)              14
