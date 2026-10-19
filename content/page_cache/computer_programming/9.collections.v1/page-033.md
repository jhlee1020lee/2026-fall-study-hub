---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
Iterator Example
                                     Note: the LinkedList constructor accepts a Collection.


 List<Integer> list = new LinkedList<>(Arrays.asList(1, 2, 3, 4, 5));
 Iterator<Integer> iterator = list.iterator();

 while (iterator.hasNext()) {
     int i = iterator.next();
     if (i == 2 || i == 4) { iterator.remove(); }
 }
 for (int e : list) { System.out.print(e + " "); }
 System.out.println();

 1 3 5

                               Jaemin Yoo (SNU)                                          33
