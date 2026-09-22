---
course: "computer_programming"
source_pdf: "Lab02.v4.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf"
generated_at: "2026-09-22T04:21:28Z"
---
Recap: Multi-Dimensional Array
Main Function

int[][] myNumbers = {{1, 2, 3}, {4, 5}};
for (int row = 0; row < myNumbers.length; ++row) {
   for (int col = 0; col < myNumbers[row].length; ++col) {
       System.out.println(myNumbers[row][col]);
   }
}

    Output
1
2
3
4
                                                             9
5
