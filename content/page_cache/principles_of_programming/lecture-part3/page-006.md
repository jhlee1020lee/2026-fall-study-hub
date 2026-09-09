---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Problems with OOP
1. Needs “subtyping” like “OInt <: Ord[OInt]”, which is quite
   complex as we have seen (and moreover, involves more
   complex concepts like variance).

2. Needs a wrapper class like “OInt” in order to add a new
   interface to an existing type like “Int”.

3. Interface only contains only “elimination” functions, not
   “introduction” functions.

4. No canonical operator

5. …
