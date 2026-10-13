---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 37
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
  Linearity of Expectations
• Theorem: If Xi, i = 1, 2, …,n with n a positive integer, are random variables on S, and if a1,
  a2, …, an and b are real numbers, then
                 𝐸 𝑎1 𝑋1 + ⋯ + 𝑎𝑛 𝑋𝑛 + 𝑏 = 𝑎1 𝐸 𝑋1 + ⋯ + 𝑎𝑛 𝐸 𝑋𝑛 + 𝑏


• Example: Expected Value in the Hatcheck Problem - A new employee started a job
  checking hats, but forgot to put the claim check numbers on the hats. So, the n
  customers just receive a random hat from those remaining. What is the expected
  number of hat returned correctly?
  – Let X be the random variable that equals the number of people who receive the correct hat
  – Xi = 1 if the i-th person receives the correct hat and Xi = 0 otherwise.
  – Note that X = X1 + X2 + ∙∙∙ + Xn,
