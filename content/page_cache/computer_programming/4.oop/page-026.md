---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 26
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Explicit Use of this

 class Car {
    int speed = 30;

     void cantChangeSpeed(int speed) {
         speed = speed;                            // does it work?
     }

     void changeSpeed(int speed) {
         this.speed = speed;                       // does it work?
     }
 }

                                Jaemin Yoo (SNU)                      26
