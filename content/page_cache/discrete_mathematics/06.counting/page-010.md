---
course: "discrete_mathematics"
source_pdf: "06.Counting.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/06.Counting.pdf"
generated_at: "2026-10-07T01:00:49Z"
---
 Recursive Algorithms
• Definition: An algorithm is called recursive if it solves a problem by reducing it to an
  instance of the same problem with smaller input.
• For the algorithm to terminate, the instance of the problem must eventually be reduced
  to some initial case for which the solution is known.
• Example: Give a recursive algorithm for computing n!, where n is a nonnegative integer.


                      procedure factorial(n: nonnegative integer)
                           if n = 0 then return 1
                           else return n·factorial (n − 1)
