---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
 Check Digits
• Universal Product Codes (UPCs) usually have 12 decimal digits, the last one being the check digit
       3𝑥1 + 𝑥2 + 3𝑥3 + 𝑥4 + 3𝑥5 + 𝑥6 + 3𝑥7 + 𝑥8 + 3𝑥9 + 𝑥10 + 3𝑥11 + 𝑥12 ≡ 0 mod 10


  – Suppose first 11 digits: 0 3 6 0 0 0 2 9 1 4 5
        3 0 + 3 + 3 6 + 0 + 3 0 + 0 + 3 2 + 9 + 3 1 + 4 + 3 5 = 8 mod 10
     We want: 58 + 𝑥12 ≡ 0 mod 10 , so: 𝑥12 = 2
     Final UPC: 036000291452


• Books are identified by an International Standard Book Number (ISBN-10), a 10 digit code.
   – The last digit is a check digit determined by: 𝑥10 ≡ σ9𝑖=1 𝑖𝑥𝑖 mod 11
   – A single error is an error in one digit of an identification number and a transposition error is the
    accidental interchanging of two digits. Both can be detected by the check digit for ISBN-10.
