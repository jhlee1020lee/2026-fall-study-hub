---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 40
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Example: Finding Max Number
• What does the code below print?


 int[] nums = {23, -43, -25, 14, 36};
 int max = Integer.MIN_VALUE; // -2147483648
 for (int num : nums) {
    if (num > max) {
        max = num;
    }
 }
 System.out.println("The max number is " + max);

                             Jaemin Yoo (SNU)      40
