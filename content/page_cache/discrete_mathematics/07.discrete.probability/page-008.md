---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
The Probability of Complements and Unions of Events
• Theorem: Let E1 and E2 be events in the sample space S. Then
          𝑝 𝐸1 ∪ 𝐸2 = 𝑝 𝐸1 + 𝑝 𝐸2 − 𝑝 𝐸1 ∩ 𝐸2
• Proof: The inclusion-exclusion formula 𝐴 ∪ 𝐵 = 𝐴 + 𝐵 − 𝐴 ∩ 𝐵

• Example: What is the probability that a positive integer selected at random from the set
  of positive integers not exceeding 100 is divisible by either 2 or 5?
• Solution: Let E1 be the event that the integer is divisible by 2 and E2 be the event that
  it is divisible 5. Then the event that the integer is divisible by 2 or 5 is E1 ∪ E2 and E1 ∩ E2
  is the event that it is divisible by 2 and 5. It follows that:
                                                                50     20       10     3
             𝑝 𝐸1 ∪ 𝐸2 = 𝑝 𝐸1 + 𝑝 𝐸2 − 𝑝 𝐸1 ∩ 𝐸2 =                  +       −       =
                                                               100 100 100 5
