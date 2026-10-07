---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 49
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Casting: Downcasting
• ClassCastException if casted to an incompatible class.
  • Downcasting is rarely used.

    class Life { public void breed(){} }
    class Animal extends Life {
        public void move(){}
    }


    Life mylife = new Life();
    ((Animal) mylife).move();

    // java.lang.ClassCastException: class Life cannot be cast to class Animal


                                     Jaemin Yoo (SNU)                            49
