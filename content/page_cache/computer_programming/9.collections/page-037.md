---
course: "computer_programming"
source_pdf: "9.collections.pdf"
pdf_page: 37
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.pdf"
generated_at: "2026-10-13T15:42:46Z"
---
Safe Deletion with Iterator

 List<String> al = new ArrayList<>();
 al.add("Hello"); al.add("World");
 al.add("Nice"); al.add("to");

 Iterator<String> iter = al.iterator();
 while (iter.hasNext()) {
    String str = iter.next();
    if (someCondition) iter.remove();
 }



                                  Jaemin Yoo (SNU)   37
