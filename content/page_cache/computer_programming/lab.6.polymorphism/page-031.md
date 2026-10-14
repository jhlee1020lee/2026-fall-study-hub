---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
  5 mins

  Problem3.1 - Scheduler
  Scheduler class defined under unknown type variable T.
   ● Scheduler<Worker> : worker group scheduler
   ● On schedule(), it samples one of the T from the group with its internal policy
     and returns it.
   ● Scheduler need not know further knowledge about the input type T.



public class Scheduler<T> {}
