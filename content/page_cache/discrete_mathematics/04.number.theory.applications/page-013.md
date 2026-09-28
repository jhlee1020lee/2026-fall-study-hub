---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
  Error Correcting Codes – Erasure Errors
• Answer: we can encode 𝑛 packets into a redundant encoding consisting of only 𝑛 + 𝑘 packets
  – Step 1: Encode data as a polynomial
  Assume that initial messages are integers 𝑎0 , 𝑎1 , … , 𝑎𝑛−1 modulo 𝑞, where 𝑞 is a prime.
  Build 𝑃 𝑋 ≔ 𝑎0 + 𝑎1 𝑋 + ⋯ + 𝑎𝑛−1 𝑋 𝑛−1 , which is a polynomial in ℤ𝑞 𝑋 of degree less than 𝑛.
  – Step 2: Generate encoded packets
  Pick 𝑛 + 𝑘 distinct values: 𝛽1 , … , 𝛽𝑛+𝑘 (1,2,3,4,5,6,7,…), then compute: 𝑐𝑖 = 𝑃 𝛽𝑖 .
  These are the transmitted packets.
  – Step 3: How to recover data?
  Key fact: A degree 𝑛 − 1 polynomial is uniquely determined by 𝑛 points
  Even if up to 𝑘 packets are lost, you can reconstruct 𝑃 𝑋 (via interpolation) as long as you still
  have any 𝑛 packets.
  Then recover: 𝑎0 , 𝑎1 , … , 𝑎𝑛−1
