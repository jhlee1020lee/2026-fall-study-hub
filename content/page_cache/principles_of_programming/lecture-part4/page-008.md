---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Can we not have both? Mutability with Ownership!

 ➢ Immutable array                ➢ Mutation with Ownership
                                   // own
   arr = Array.new([1;2;3])        arr = Array.new([1;2;3])

   … using arr …                   … using arr …
                                   // mutable borrow
   arr’ = Array.set(arr, 0, 42)    Array.set(&mut arr, 0, 42)
                                   // immutable borrow
   f(arr’)                         f(&arr)

   … using arr’ …                  … using arr …

   g()                             g()

   … using arr’ …                  … using arr …
