---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
 Recursively Defined Functions
• Def: A recursive or inductive definition of a function consists of two steps.
  – BASIS STEP: Specify the value of the function at zero.
  – RECURSIVE STEP: Give a rule for finding its value at an integer from its values at smaller
   integers.


• Examples
  – 𝑓 0 = 3 and 𝑓 𝑛 + 1 = 2𝑓 𝑛 + 3 for 𝑛 ≥ 0
  – A recursive definition of 𝑠𝑛 = σ𝑛𝑘=0 𝑎𝑘 is: 𝑠0 = 𝑎0 and 𝑠𝑛+1 = 𝑠𝑛 + 𝑎𝑛+1 for 𝑛 ≥ 0
  – Fibonacci numbers: 𝑓0 = 𝑓1 = 1 and 𝑓𝑛 = 𝑓𝑛−1 + 𝑓𝑛−2 for 𝑛 ≥ 2
