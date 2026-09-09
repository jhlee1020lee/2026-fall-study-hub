---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 7
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Immutability for Guarantee & Mutability for Efficiency

 ➢ Immutable array                ➢ Mutable array

   arr = Array.new([1;2;3])        arr = Array.new([1;2;3])

   … using arr …                   … using arr …

   arr’ = Array.set(arr, 0, 42)    Array.set(arr, 0, 42);

   f(arr’)                         f(arr)

   … using arr’ …                  … using arr …

   g()                             g()

   … using arr’ …                  … using arr …
