---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 64
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Lower-Bounded Wildcards <? super>
• Restrict the type to be a supertype of a class.

  public static void addNumbers(List<? super Integer> list) {
     for (Object n : list) {
         System.out.print(n.toString() + " ");
     }
  }

  List<Integer> l1 = Arrays.asList(1, 2, 3);
  addNumbers(l1);                                       // 1 2 3
  List<Number> l2 = Arrays.asList(1.0, 2.0, 3.0);
  addNumbers(l2);                                       // 1.0 2.0 3.0


                                   Jaemin Yoo (SNU)                      64
