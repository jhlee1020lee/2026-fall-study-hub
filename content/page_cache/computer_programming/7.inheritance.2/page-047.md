---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 47
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
default and static Methods
• Starting from Java 8, default / static methods (with body) are
  allowed in the interface (different from the “default” modifier).

   interface RamenCooker {
       void boilWater();

       default void clean() {
           System.out.println("Rinsing with water");
       }
   }

                               Jaemin Yoo (SNU)                       47
