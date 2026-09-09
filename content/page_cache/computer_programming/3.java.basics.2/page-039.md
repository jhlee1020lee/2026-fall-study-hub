---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 39
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Example: Nested Loop
• What does the code below print?


 for (int i = 5; i > 0; i--) {
    for (int j = 0; j < i; j++) {
        // System.out.print doesn't break line
        System.out.print("*");
    }
    System.out.println();
 }

                             Jaemin Yoo (SNU)    39
