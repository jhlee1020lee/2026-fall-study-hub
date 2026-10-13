---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Conditional Probability
• Definition: Let E and F be events with p(F) > 0. The conditional probability of E given F,
  denoted by P(E|F), is defined as:
                                                𝑝 𝐸∩𝐹
                                    𝑝 𝐸 𝐹) =
                                                  𝑝 𝐹

• Example: A bit string of length four is generated at random so that each of the 16 bit
  strings of length 4 is equally likely. What is the probability that it contains at least two
  consecutive 0s, given that its first bit is a 0?
• Solution: Let E be the event that the bit string contains at least two consecutive 0s, and
  F be the event that the first bit is a 0.
  – Since E ⋂ F = {0000, 0001, 0010, 0011, 0100}, p(E⋂F) = 5/16.
  – Because 8 bit strings of length 4 start with a 0, p(F) = 8/16= ½ .
  – Hence, p(E | F) = 5/8
