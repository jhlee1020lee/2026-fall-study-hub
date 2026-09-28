---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
 Secret Sharing
• Secret Sharing
  – We want to devise a 𝑘-out-of-𝑛 secret sharing scheme such that (1) any group of 𝑘 of these
   officials can pool their information to figure out the code but (2) any group of 𝑘 − 1 or fewer have
   no information about the code, even if they pool their knowledge.


• Example: polynomial encoding
  – Pick a random polynomial 𝑃 𝑋 ∈ ℤ𝑞 𝑋 of degree < 𝑘 such that 𝑃 0 = 𝑠.
  – Give 𝑃 𝑖 to the 𝑖-th official.
  – Now any 𝑘 officials can use Lagrange interpolation to recover 𝑃 𝑥 , then compute 𝑃 0 = 𝑠.
  – Any group of fewer than 𝑘 officials learns no information about 𝑠 (why?)
