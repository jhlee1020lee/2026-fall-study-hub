---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 85
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Multiple Inheritance Problem
Ø Multiple Inheritance
  • The famous “diamond problem”

   class A(val a: Int)
   class B extends A(10)
   class C extends A(20)
   class D extends B, C.

   Problem 1: What is the value of (new D).a ?

   Problem 2: The constructor of A must be executed once
              because A may contain side effects such as
              sending messages over the network.
