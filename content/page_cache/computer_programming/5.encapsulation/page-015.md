---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
private Methods

 AppleStore store = new AppleStore();

 System.out.println("< Initial Balance and Stock>");
 System.out.println(store.getBalance() + ", " + store.getStock());

 boolean success = store.sell(50);
 if (success) {
    System.out.println("< After selling apples >");
    System.out.println(store.getBalance() + ", " + store.getStock());
 } else {
    System.out.println("Not enough apples in stock");
 }


                                  Jaemin Yoo (SNU)                      15
