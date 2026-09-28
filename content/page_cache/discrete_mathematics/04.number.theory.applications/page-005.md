---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
 Public-key Cryptography
• Public-key Cryptography
   – Knowing how to encrypt a message does not help decrypt ciphertexts
   – Therefore, everyone can have a publicly known encryption key (public key). The only key that needs to be kept
     secret is the decryption key (secret key)

• Public-key Encryption
   – Bob publishes his public key 𝐾𝑝𝑢𝑏
   – Alice encrypts message: 𝐶 = 𝐸𝐾𝑝𝑢𝑏 𝑀
   – Only Bob can decrypt using his private key 𝐾𝑝𝑟𝑖𝑣

• Examples
   – Starting point: Merkle (1974)
   – The Diffie-Hellman key-exchange protocol (1976): discrete logarithm problem 𝑔 𝑥 = ℎ mod 𝑝
   – The RSA encryption (1977): integer factorization problem 𝑁 = 𝑝𝑞 for large primes 𝑝, 𝑞
