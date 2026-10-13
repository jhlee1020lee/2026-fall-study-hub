---
course: "computer_programming"
source_pdf: "9.collections.pdf"
pdf_page: 44
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.pdf"
generated_at: "2026-10-13T15:42:46Z"
---
Set Operation Example 2
Set setA = new HashSet(),
    setB = new HashSet();
for (int i = 0; i < 7; i++) { setA.add(i); }
for (int i = 4; i < 11; i++) { setB.add(i); }
System.out.println(setA);
setA.addAll(setB);
System.out.println(setA);
setA.removeAll(setB);
System.out.println(setA);

[0, 1, 2, 3, 4, 5, 6]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
[0, 1, 2, 3]

                                      Jaemin Yoo (SNU)   44
