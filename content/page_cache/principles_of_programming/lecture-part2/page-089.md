---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 89
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Algorithm for Multiple Inheritance
ØAlgorithm
  • Give a linear order among all ancestors by “post-order” traversing
    without revisiting the same node.
  • Invoke the constructors once in that order.
    Note. Post-order traversal of a class C means
     − Recursively post-order traverse C’s first parent; …;
     − Recursively post-order traverse C’s last parent; and
     − Visit C.
     By post-order traversing from “E” in the previous example,
     we have the order: A(10) -> B -> C -> D -> E
    val e = new E
    e.a // 10                     e.f(100) // 100*10
    e.g(100) // 100 + 10          e.h(100) // (100 + 50) * 10
  • A constructor with arguments is always visited before the same
    constructor with no arguments.
  • Compile error if the same field is implemented by multiple classes
