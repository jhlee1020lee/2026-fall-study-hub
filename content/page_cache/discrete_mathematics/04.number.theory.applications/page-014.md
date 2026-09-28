---
course: "discrete_mathematics"
source_pdf: "04.Number.Theory.Applications.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/04.Number.Theory.Applications.pdf"
generated_at: "2026-09-28T00:49:38Z"
---
   Error Correcting Codes – General Errors
• General errors
  – Alice wishes to communicate with Bob over a noisy channel.
  – Her messages are 𝑎0 , … , 𝑎𝑛−1 . Some of the messages would be corrupted during transmission.
  – Bob receives 𝑛 messages as Alice transmits, but 𝑘 of them are corrupted and Bob has no idea which 𝑘
  – Recovering from such general errors is much more challenging than erasure errors


• As before, we describe the message by a polynomial 𝑃 𝑋 = 𝑎0 + 𝑎1 𝑋 + ⋯ + 𝑎𝑛−1 𝑋 𝑛−1 ∈ ℤ𝑞 𝑋
  – Question: how many extra evaluations are needed to tolerate up to 𝑘 general errors?
  – Answer: Alice must transmit 2𝑘 extra evaluations of 𝑃 𝑋 (as opposed to just 𝑘 additional packets in
   the case of erasures).
  – Thus the encoded message is 𝑐1 = 𝑃 𝛽1 , … , 𝑐𝑛+2𝑘 = 𝑃 𝛽𝑛+2𝑘 for some fixed 𝛽1 , … , 𝛽𝑛+2𝑘 ∈ ℤ𝑞
