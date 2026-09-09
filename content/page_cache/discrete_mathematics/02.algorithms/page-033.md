---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Big-Omega Notation
• Def: Let f and g be functions from the set of integers or the set of real numbers to the
  set of real numbers. We say that f(x) = Ω(g(x)) if there are constants C and k such that
  |f(x)| ≥ C |g(x)| whenever x > k.

  – We say that “f(x) is big-Omega of g(x).”
  – Big-O gives an upper bound on the growth of a function, while Big-Omega gives a lower
   bound. Big-Omega tells us that a function grows at least as fast as another.
  – f(x) = Ω(g(x)) if and only if g(x) = O(f(x)). This follows from the definitions.
