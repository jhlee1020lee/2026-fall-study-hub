---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 59
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Advantages: Robustness
• Resolving types are all done in compile-time.
• Runtime type error does not occur at all, and it is robust.

  import java.util.ArrayList;
  import java.util.List;

  List<String> list = new ArrayList<>();
  list.add("Compile");
  list.add(11235);

  // java: incompatible types: int cannot be converted to java.lang.String


                                      Jaemin Yoo (SNU)                       59
