---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Why Polymorphism?
• How should we avoid different methods for a similar action?

    class Animal {
       public void move() { System.out.println("Move!"); }
    }
    class Fish extends Animal {
       public void swim() { System.out.println("Swim!"); }
    }

    Animal a = new Fish();
    a.move();
    ((Fish)a).swim();


                                  Jaemin Yoo (SNU)              6
