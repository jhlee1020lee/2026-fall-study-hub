---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 37
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Breaking Loop
• There are two ways to break a loop during iterations.
   • continue; break the current iteration and go to the next iteration.
   • break; break out of the entire loop. It is similar to break in switch.


 for (int i = 0; i < 5; i++) {
    if (i == 3) {
        break;         // what if it changes to continue?
    }
    System.out.println(i);
 }

                                     Jaemin Yoo (SNU)                         37
