---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
 Check Digits
• Error check
   – A common technique for detecting errors in strings is to add an extra digit to the end of the string
   – The final digit (check digit) is calculated using a particular function. To determine whether a digit
    string is correct, a check is made to see whether this final digit has the correct value
   – A simple example: parity check bits
     Count number of 1s and make total number of 1s even
     Data: 1011001 (number of 1s = 4 → already even)
     Check bit = 0
     Final transmitted: 10110010
     If error happens:
            Received: 10110011 (now 5 ones → odd            )
      Error detected!
