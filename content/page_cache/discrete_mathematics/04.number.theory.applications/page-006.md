---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
Rivest-Shamir-Adleman (RSA)
• The RSA Cryptosystem
  – Key generation: 𝑁 = 𝑝𝑞 where 𝑝, 𝑞 are large prime numbers. Choose an integer 𝑒 relatively prime
   to 𝜙 𝑁 = 𝑝 − 1 𝑞 − 1 , and let 𝑑 = 𝑒 −1 mod 𝜙 𝑛 . Set 𝑝𝑘 = 𝑁, 𝑒 and 𝑠𝑘 = 𝑁, 𝑑 .
  – Encryption: Encpk 𝑚 = 𝑚𝑒 mod 𝑁
  – Decryption: Decsk 𝑐 = 𝑐 𝑑 mod 𝑁


• Correctness:
  – Euler’s theorem
                                     𝑚𝜑 𝑁 ≡ 1 mod 𝑁
  – Because: 𝑒𝑑 ≡ 1 mod 𝜑 𝑁 , we have: 𝑚𝑒𝑑 ≡ 𝑚 mod 𝑁
