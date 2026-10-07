---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 62
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Upper-Bounded Wildcards <? extends>
• Restrict the type to be a subtype of a class.

  import java.util.ArrayList;
  private static Double reduce(ArrayList<? extends Number> num) {
     double sum=0.0;
     for(Number n:num) { sum = sum + n.doubleValue(); }
     return sum;
  }

  ArrayList<Integer> l1 = new ArrayList<>();
  l1.add(10); l1.add(20);
  System.out.println("sumint "+reduce(l1));             // sumint 30.0


                                   Jaemin Yoo (SNU)                      62
