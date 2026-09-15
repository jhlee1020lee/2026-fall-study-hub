---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Motivation: Example Code
• An external user must know the exact mechanism of an object.

  class FruitStore {
     int balance = 10000;
     int stock = 30;
  }

  FruitStore store = new FruitStore();
  System.out.println(store.stock + " " + store.balance);
  store.stock -= 3;
  store.balance += 2000 * 3;              // Intended behavior of SELL
  System.out.printf(store.stock + " " + store.balance);

                                  Jaemin Yoo (SNU)                       4
