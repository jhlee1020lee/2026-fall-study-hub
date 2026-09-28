---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
 Full Binary Trees
• Def: The height h(T) of a full binary tree T is defined recursively as follows:
  – BASIS STEP: The height of a full binary tree T consisting of only a root r is h(T) = 0.
  – RECURSIVE STEP: If T1 and T2 are full binary trees, then the full binary tree T = T1∙T2
   has height h(T) = 1 + max{h(T1), h(T2)}

• Def: The number of vertices n(T) of a full binary tree T satisfies the following:
  – BASIS STEP: The number of vertices of a full binary tree T consisting of only a root r is
   n(T) = 1.
  – RECURSIVE STEP: If T1 and T2 are full binary trees, then the full binary tree T = T1∙T2
   has the number of vertices n(T) = 1 + n(T1) + n(T2)

• Thm: If T is a full binary tree, then n(T) ≤ 2h(T)+1 – 1.
