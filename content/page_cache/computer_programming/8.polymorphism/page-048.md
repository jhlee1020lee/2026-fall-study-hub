---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 48
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Casting: Upcasting
• A variable of type T can hold an object of any subclass of T.
   • Decoupling the derived class implementation from its abstraction.


  // explicit upcasting
  Employee e = (Employee)(new Executive());
  Animal a = (Animal)(new Beagle());

  // implicit upcasting
  Employee e = new Executive();
  Animal a = new Beagle();

                                  Jaemin Yoo (SNU)                       48
