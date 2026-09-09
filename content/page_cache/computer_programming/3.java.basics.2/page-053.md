---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 53
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Function Orders Does NOT Matter!
• Declaration order of functions doesn’t matter in Java.


    class Main {
       void first() { second(); }
                                                  “second” is declared below
        void second() { third(); }                this line, but doesn’t matter.


        void third() { System.out.println("third"); }
    }

                               Jaemin Yoo (SNU)                                    53
