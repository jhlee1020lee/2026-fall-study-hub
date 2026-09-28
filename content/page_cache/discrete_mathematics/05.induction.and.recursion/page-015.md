---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
 Rooted Trees
• Definition: The set of rooted trees, where a rooted tree consists of a set of vertices
  containing a distinguished vertex called the root, and edges connecting these vertices,
  can be defined recursively by these steps:
  BASIS STEP: A single vertex r is a rooted tree.
  RECURSIVE STEP: Suppose that T1, T2, …,Tn are disjoint rooted trees with roots r1,
   r2,…,rn, respectively. Then the graph formed by starting with a root r, which is not in
   any of the rooted trees T1, T2, …,Tn, and adding an edge from r to each of the vertices
   r1, r2,…,rn, is also a rooted tree.
