---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 57
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Generic Methods
• A method declaring one or more type variables.
  • Type arguments may either be inferred or passed explicitly.


  Integer[] intArray = { 1, 1, 2, 3, 5, 8, 13 };
  Character[] charArray = { 'C', 'S', 'E', 'C', 'P' };
  ArrayPrinter.printArray(intArray);
  ArrayPrinter.<Character>printArray(charArray);

  1 1 2 3 5 8 13
  C S E C P

                                  Jaemin Yoo (SNU)                57
