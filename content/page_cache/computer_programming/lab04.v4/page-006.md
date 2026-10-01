---
course: "computer_programming"
source_pdf: "Lab04.v4.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf"
generated_at: "2026-10-01T16:19:03Z"
---
Access Modifiers
● Access modifier private
  Class Definition
  class Pizza {
     private String topping = “Pineapple”;
  }                      Not accessible by other classes

  main Method
  Pizza hawaiian = new Pizza();
  System.out.println(hawaiian.topping);

  Output
  java: topping has private access in Pizza

                                                           6
