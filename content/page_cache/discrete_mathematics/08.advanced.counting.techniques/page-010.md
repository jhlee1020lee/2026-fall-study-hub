---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
 Examples
• What is the solution to the recurrence relation an = an−1 + 2an−2 with a0 = 2 and a1 = 7?
  – The characteristic equation is r2 − r − 2 = 0. Its roots are r = 2 and r = −1 . Therefore, {an} is a
    solution to the recurrence relation if and only if an = α12n + α2(−1)n, for some constants α1 and α2.
  – To find the constants α1 and α2, note that a0 = 2 = α1 + α2 and a1 = 7 = α12 + α2(−1). Solving these
    equations, we find that α1 = 3 and α2 = −1.
  – Hence, the solution is the sequence {an} with an = 3∙2n − (−1)n.


• What is the solution to the recurrence relation an = 6an−1 − 9an−2 with a0 = 1 and a1 = 6?
  – The characteristic equation is r2 − 6r + 9 = 0. The only root is r = 3. Therefore, {an} is a solution to
   the recurrence relation if and only if an = α13n + α2n3n where α1 and α2 are constants.
  – To find the constants α1 and α2, note that a0 = 1 = α1 and a1 = 6 = α1 ∙ 3 + α2 ∙3. Solving, we find
   that α1 = 1 and α2 = 1. Hence, an = 3n + n3n.
