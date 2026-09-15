---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Encapsulation with private Attributes

 AppleStore store = new AppleStore();
 System.out.println("< Initial balance and stock>");
 System.out.println(
        store.getBalance() + ", " + store.getStock());
 store.sell(3);
 System.out.println("< After selling 3 apples >");
 System.out.println(store.getBalance() + ", " + store.getStock());

 < Initial balance and stock>
 10000, 30
 < After selling 3 apples >
 16000, 27


                                 Jaemin Yoo (SNU)                    12
