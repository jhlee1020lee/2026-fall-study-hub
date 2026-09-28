---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 2
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
Hashing Functions
• Hash functions are simply functions that take inputs of some (arbitrary) length and
  compress them into short, fixed-length outputs
  – One of the most common examples: 𝐻 𝑥 = 𝑥 mod 𝑚


• The classic use of hash functions is in data structures
  – A hash function assigns memory location 𝐻 𝑥 to the record 𝑥 so that it can be retrieved quickly
  – Hash tables can be built to enable a constant lookup time
  – Hash functions are not one-to-one, more than one item may be assigned to a memory location
  – A “good” hash function is one that yields few collisions
