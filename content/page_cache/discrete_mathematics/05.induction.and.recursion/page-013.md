---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
 String Concatenation
• Def: Two strings can be combined via the operation of concatenation. Let Σ be a set of
  symbols and Σ* be the set of strings formed from the symbols in Σ. We can define the
  concatenation of two strings, denoted by ∙, recursively as follows.
  BASIS STEP: If w  Σ*, then w ∙ λ= w.
  RECURSIVE STEP: If w1  Σ* and w2  Σ* and x  Σ, then w1 ∙ (w2 x)= (w1 ∙ w2)x.


  – Often w1 ∙ w2 is written as w1 w2.
  – If w1 = abra and w2 = cadabra, the concatenation       w1 w2 = abracadabra.
