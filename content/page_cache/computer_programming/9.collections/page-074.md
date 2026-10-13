---
course: "computer_programming"
source_pdf: "9.collections.pdf"
pdf_page: 74
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.pdf"
generated_at: "2026-10-13T15:42:46Z"
---
Utilities Example: Others

List list = Arrays.asList("one Two three Four five six one".split(" "));
Collections.reverse(list);
System.out.println("reverse: " + list); // [one, six, five, Four, three, Two, one]
Collections.rotate(list, 3);
System.out.println("rotate: " + list);    // [three, Two, one, one, six, five, Four]

List source = Arrays.asList("in the matrix".split(" "));
Collections.copy(list, source);
System.out.println("copy: " + list);      // [in, the, matrix, one, six, five, Four]
Collections.swap(list, 0, list.size() - 1);
System.out.println("swap: " + list);      // [Four, the, matrix, one, six, five, in]
Collections.fill(list, "pop");
System.out.println("fill: " + list);      // [pop, pop, pop, pop, pop, pop, pop]


                                          Jaemin Yoo (SNU)                             74
