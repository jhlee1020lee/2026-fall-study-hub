---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 65
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Unbounded Wildcards <?>
• Represent an arbitrary type.

  import java.util.Collection;
  static void printCollection(Collection<?> c) {
     for (Object o : c) { System.out.println(o); }
  }


  Collection<String> cs = new ArrayList<String>();
  cs.add("hello");
  cs.add("world");
  printCollection(cs);

                                 Jaemin Yoo (SNU)    65
