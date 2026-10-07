---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 50
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Why Downcasting?
• Explicitly downcast to access extended methods of subclass.

  class Life { public void breed() { } }
  class Animal extends Life { public void move() { } }



  Life mylife = new Animal();

  mylife.move();                            // not okay
  ((Animal) mylife).move();                 // okay

                                Jaemin Yoo (SNU)                50
