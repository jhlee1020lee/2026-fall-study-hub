---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
  Applying Bayes’ Theorem – (a)
• Example: Suppose that one person in 100,000 has a particular disease. There is a test for
  the disease that gives a positive result 99% of the time when given to someone with the
  disease. When given to someone without the disease, 99.5% of the time it gives a negative
  result. Find
  a) the probability that a person who test positive has the disease (true positive)

• Let 𝐷 be the event that the person has the disease, and 𝐸 the event that this person tests
  positive. We need to compute 𝑝 𝐷 𝐸)
  – We know that 𝑝 𝐷 = 10−5 , 𝑝 𝐸 𝐷) = 0.99, 𝑝 𝐸 𝐷 = 0.995
                                          𝑝 𝐸 𝐷) 𝑝(𝐷)                   (0.99)(0.00001)
  – By Bayes’ Theorem, 𝑝 𝐷     𝐸) =                         =                                  ≈ 0.002
                                    𝑝 𝐸 𝐷) 𝑝 𝐷 +𝑝 𝐸 𝐷)𝑝 𝐷       0.99 0.00001 +(0.005)(0.99999)

• So, don’t worry too much, if your test for this disease comes back positive.
  – Can you use this formula to explain why the resulting probability is surprisingly small?
