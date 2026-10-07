---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Constructor Overloading Rules
• Calling another constructor must be the first thing it does.
• Why?
   • this() delegates initialization to another constructor.
   • Requiring it first ensures that the delegated constructor finishes before
     the remaining code uses the object.
   • This gives a predictable order: initialize first, then perform the work.
   • Java 25 allows restricted work beforehand (not that important).




                                   Jaemin Yoo (SNU)                              19
