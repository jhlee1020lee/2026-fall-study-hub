---
course: "computer_programming"
source_pdf: "9.collections.pdf"
pdf_page: 36
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.pdf"
generated_at: "2026-10-13T15:42:46Z"
---
Element Deletion Error
• The for loop uses an iterator internally.
   • However, removing an element directly can cause an error.

 List<String> al = new ArrayList<>();

 al.add("Hello");
 al.add("World");
 al.add("Nice");
 al.add("to");

 for (String str : al) {
    if (someCondition) al.remove(str);         // ConcurrentModificationException
 }

                                   Jaemin Yoo (SNU)                                 36
