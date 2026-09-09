---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 87
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Scala’s Solution: Trait
ØTraits
  • A trait can implement any of its methods,
    but should have only one constructor with no arguments.
  • An [abstract] class (resp. trait) X can
    “extends” one trait or [abstract] class with any (resp. no) arguments
    “with” multiple traits T1 , … , Tn
    such that, for each i,
    the least superclass of Ti, if exists, should be a superclass of X
    where
    C is a superclass of T if C is an (abstract) class and T transitively
    “extends” C.
  • No cyclic inheritance is allowed.
ØProperty
  • For any ancestor class in the inheritance tree of a class:
    - Its constructor with arguments can appear at most once
    - Its constructor with no argument can appear multiple times
