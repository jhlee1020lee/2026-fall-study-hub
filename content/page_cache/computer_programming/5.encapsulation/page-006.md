---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Motivation: Example Code
• People can use the object easier, in a more expected manner.
  • Unauthorized access to internal data may cause unexpected behavior.



  FruitStore store = new FruitStore();
  System.out.println(store.stock + " " + store.balance);
  store.stock -= 3;
  System.out.printf(store.stock + " " + store.balance);




                                Jaemin Yoo (SNU)                          6
