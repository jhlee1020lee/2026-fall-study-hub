---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
 Error Correcting Codes – General Errors
• Let 𝑐1 = 𝑃 𝛽1 , … , 𝑐𝑛+2𝑘 = 𝑃 𝛽𝑛+2𝑘 be the encoded message
                  ′        ′                                                                     ′
  – Bob received 𝑐1 , … , 𝑐𝑛+2𝑘 ∈ ℤ𝑞 , and at least 𝑛 + 𝑘 of these values are uncorrupted (𝑐𝑖 = 𝑐𝑖 )


• Goal: find a polynomial 𝑄 𝑋 of degree < 𝑛 such that 𝑄 𝛽𝑖 = 𝑐𝑖′ for at least 𝑛 + 𝑘 points.


• Uniqueness: why is this enough?
  – Let 𝑄 𝑋 be a polynomial of degree < 𝑛 such that 𝑄 𝛽𝑖 = 𝑐𝑖′ at 𝑛 + 𝑘 points
  – Among these 𝑛 + 𝑘 points, there are at most 𝑘 errors
  – We must have 𝑃 𝛽𝑖 = 𝑐𝑖 = 𝑄 𝛽𝑖 on at least 𝑛 points, and therefore 𝑃 𝑋 ≡ 𝑄 𝑋 .


• But how can Bob quickly find such a polynomial?
  – The issue at hand is the locations of the 𝑘 errors.
