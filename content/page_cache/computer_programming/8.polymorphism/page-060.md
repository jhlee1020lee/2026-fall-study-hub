---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 60
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Advantages: No Type Casting

 import java.util.ArrayList;
 import java.util.List;


 List list = new ArrayList();
 list.add("String");
 System.out.println(((String)list.get(0)).toUpperCase());


 List<String> list = new ArrayList<>();
 list.add("String");
 System.out.println(list.get(0).toUpperCase());


                                  Jaemin Yoo (SNU)          60
