---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Motivation: Example Code
• What if we share a method “sell”?

  class FruitStore {
     int balance = 10000;
     int stock = 30;

      void sell (int num) {
          balance += 2000 * num;
          stock -= num;
      }
  }

                                   Jaemin Yoo (SNU)   5
