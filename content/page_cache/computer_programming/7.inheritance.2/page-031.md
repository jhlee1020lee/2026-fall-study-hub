---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Interface Example
interface PizzaStore {
   public Pizza bakePizza();
   public void deliver();
}

class PizzaHut implements PizzaStore {       class MrPizza implements PizzaStore {
   public Pizza bakePizza(){                    public Pizza bakePizza() {
       addCheese();                                 addPepperoni();
   }                                            }
   public void deliver() {                      public void deliver() {
       findDeliveryLocation();                      findDeliveryMan();
   }                                            }
}                                            }

                                    Jaemin Yoo (SNU)                                 31
