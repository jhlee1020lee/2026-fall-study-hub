---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
     Recap: Generics

     Advantage 1: Robustness
          ○ Resolving types are all done in compile-time.
          ○ Runtime type error does not occur at all, and it is robust.
                List<String> list = new ArrayList<>();
                list.add("Compile");
                list.add(11235);

     Advantage 2: No type casting
List list = new ArrayList();               List<String> list = new ArrayList<>();
list.add("String");                        list.add("String");
System.out.println((String)list.get(0));   System.out.println(list.get(0));



                                                                             8
