---
course: "computer_programming"
source_pdf: "9.collections.pdf"
pdf_page: 54
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.pdf"
generated_at: "2026-10-13T15:42:46Z"
---
Comparable vs. Comparator
• To use a TreeSet, it must be possible to compare the elements
  and determine which one is “larger”.
• Method 1 (natural order):
   • Override compareTo(Object o) of the elements’ class.
• Method 2 (special order):
   • Implement a Comparator interface.




                                 Jaemin Yoo (SNU)                 54
