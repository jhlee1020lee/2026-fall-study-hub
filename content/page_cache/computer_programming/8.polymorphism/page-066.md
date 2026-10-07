---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 66
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Difference <?> between <T>
• We can rewrite the previous example using <T> instead of <?>.
  • Collection<?>: a collection of some unknown element type.
  • Collection<T>: a collection whose element type is named T.
     • You can refer to that type elsewhere.



  import java.util.Collection;
  static <T> void printCollection(Collection<T> c) {
     for (Object o : c) { System.out.println(o); }
  }


                                       Jaemin Yoo (SNU)           66
