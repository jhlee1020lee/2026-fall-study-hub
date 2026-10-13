---
course: "computer_programming"
source_pdf: "9.collections.pdf"
pdf_page: 75
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.pdf"
generated_at: "2026-10-13T15:42:46Z"
---
Utilities Example: More

List list = Arrays.asList("one Two three Four five six Four five one".split(" "));
List sublist = Arrays.asList("Four five".split(" "));

System.out.println("indexOfSubList: " +
   Collections.indexOfSubList(list, sublist));            // 3
System.out.println("lastIndexOfSubList: " +
   Collections.lastIndexOfSubList(list, sublist));        // 6

Collections.replaceAll(list, "one", "Yo");
System.out.println("replaceAll: " + list);
// [Yo, Two, three, Four, five, six, Four, five, Yo]


                                       Jaemin Yoo (SNU)                              75
