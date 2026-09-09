---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Binary Search
• Assume the input is a list of items in increasing order.


• The algorithm begins by comparing the element to be found with the middle element.
  – If the middle element is lower, the search proceeds with the upper half of the list.
  – If it is not lower, the search proceeds with the lower half of the list (through the middle
   position).


• Repeat this process until we have a list of size 1.
  – If the element we are looking for is equal to the element in the list, the position is returned.
  – Otherwise, 0 is returned to indicate that the element was not found.
