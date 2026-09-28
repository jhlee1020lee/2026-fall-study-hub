---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
  Strings
• Def: The set Σ* of strings over the alphabet Σ:
  BASIS STEP: λ ∊ Σ* (λ is the empty string)
  RECURSIVE STEP: If w is in Σ* and x is in Σ, then wx  Σ*.


• Example: If Σ = {0,1}, the strings in in Σ* are the set of all bit strings, λ,0,1, 00,01,10, 11, etc.


• Example: If Σ = {a,b}, show that aab is in Σ*.
  – Since λ ∊ Σ* and a ∊ Σ, a ∊ Σ*.
  – Since a ∊ Σ* and a ∊ Σ, aa ∊ Σ*.
  – Since aa ∊ Σ* and b ∊ Σ, aab ∊ Σ*.
