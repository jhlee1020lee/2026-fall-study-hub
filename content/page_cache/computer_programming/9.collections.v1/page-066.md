---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 66
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
boolean and void Return Types
• Queue.add() returns boolean, while Deque.addFirst() is void.
• Is there a fundamental difference? No.
  • Queue.add() inherits that signature from Collection, where a boolean
    can be useful; e.g., Set.add(x) returns false when x already exists.
  • addFirst() is a separate method, so it doesn’t have to follow it; returning
    boolean does not provide information, as it causes an exception.




                                  Jaemin Yoo (SNU)                            66
