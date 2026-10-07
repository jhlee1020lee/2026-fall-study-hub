---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Limitations of instanceof and getClass()
• Complex and hard-to-read code.
  • Non-sequential code with many branching.
• Hard to debug and maintain.
  • May forget to type check or add new types when a new class is defined.

 if (e instanceof Executive) { return 960; }
 else if(e instanceof Manager) { return 250; }
 else if(e instanceof CEO) { return 5400; }
 else if(e instanceof Cleaner) { return 150; }
 else if(e instanceof Researcher) { return 650; }
 else { return 180 };


                                      Jaemin Yoo (SNU)                       31
