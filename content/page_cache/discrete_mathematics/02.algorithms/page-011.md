---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
 Binary Search - example
Example: The steps taken by a binary search for 19 in the list:
           1 2 3 5 6 7 8 10 12 13 15 16 18 19 20 22
1. The list has 16 elements, so the midpoint is 8. The value in the 8th position is 10. Since 19 > 10, further
   search is restricted to positions 9 through 16.
           1 2 3 5 6 7 8 10 12 13 15 16 18 19 20 22
2. The midpoint of the list (positions 9 through 16) is now the 12th position with a value of 16.
           1 2 3 5 6 7 8 10 12 13 15 16 18 19 20 22
3. The midpoint of the current list is now the 14th position with a value of 19.
           1 2 3 5 6 7 8 10 12 13 15 16 18 19 20 22
4. The midpoint of the current list is now the 13th position with a value of 18.
          1 2 3 5 6 7 8 10 12 13 15 16 18 19 20 22
5. Now the list has a single element and the loop ends. Since 19=19, the location 14 is returned.
