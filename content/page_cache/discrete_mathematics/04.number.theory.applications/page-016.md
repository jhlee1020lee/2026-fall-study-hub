---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
  Error Correcting Codes – General Errors
• Decoding algorithm (Berlekamp and Welch)
  – Let 𝑒1 , … , 𝑒𝑘 ∈ 𝛽1 , … , 𝛽𝑛+2𝑘 be the 𝑘 locations at which errors occurred
  – Consider the error-locator polynomial 𝐸 𝑋 ≔ 𝑋 − 𝑒1 … 𝑋 − 𝑒𝑘 . Then:
                                𝑃 𝛽𝑖 ⋅ 𝐸 𝛽𝑖 = 𝑐𝑖′ 𝐸 𝛽𝑖 for 1 ≤ 𝑖 ≤ 𝑛 + 2𝑘.
  – Let 𝑅 𝑋 ≔ 𝑃 𝑋 ⋅ 𝐸 𝑋 , which is a polynomial of degree < 𝑛 + 𝑘. It is therefore described by 𝑛 + 𝑘
   coefficients.
  – Meanwhile, 𝐸 𝑋 is described by 𝑘 coefficients (the leading coefficient is 1)
  – Now the equations 𝑅 𝛽𝑖 = 𝑐𝑖 𝐸 𝛽𝑖 for 1 ≤ 𝑖 ≤ 𝑛 + 2𝑘 forms a linear system with 𝑛 + 2𝑘 variables.
                                                                          𝑅(𝑋)
  – We can solve the linear system and get 𝐸 𝑋    and 𝑅 𝑋 . Then, compute      to obtain 𝑃 𝑋 .
                                                                          𝐸(𝑋)



• Remark: The linear system is consistent. The solution may not be unique, but we always derive the
  same 𝑃 𝑋 (why?)
