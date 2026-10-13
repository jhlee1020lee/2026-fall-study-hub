---
course: "computer_programming"
source_pdf: "9.collections.pdf"
pdf_page: 17
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.pdf"
generated_at: "2026-10-13T15:42:46Z"
---
List Interface Example

 List<String> list = new ArrayList<>();

 list.add("Apple");            // ["Apple"]
 list.add("Banana");           // ["Apple", "Banana"]
 list.add("Carrot");           // ["Apple", "Banana", "Carrot"]

 list.remove(1);               // ["Apple", "Carrot"]
 list.size();                  // 2
 list.get(1);                  // "Carrot"
 list.contains("Banana");      // false


                               Jaemin Yoo (SNU)                   17
