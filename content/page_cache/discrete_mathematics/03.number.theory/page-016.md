---
course: "discrete_mathematics"
source_pdf: "03.Number.Theory.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/03.Number.Theory.pdf"
generated_at: "2026-09-20T23:38:11Z"
---
Primary Test
• The sieve of Erastosthenes
  – If 𝑛 is a composite integer, then it has a prime divisor less than or equal to 𝑛.
  – Trial division, a very inefficient method of determining if a number 𝑛 is prime, is to try every
   integer 𝑑 ≤ 𝑛 and see if 𝑛 is divisible by 𝑑.


• Deterministic Tests: In 2002, the first provably unconditional deterministic polynomial
  time test for primality was invented by Agrawal, Kayal, and Saxena (AKS test). There are
  several conditional/unconditional variants of AKS with better complexity.
  – The AKS primality test runs in 𝑂෨ log 𝑛 12 , improved to 𝑂෨     log 𝑛 7.5 in the revision.
  – Subsequently, Lenstra and Pomerance presented a version of the test which runs in time
   𝑂෨ log 𝑛 6
