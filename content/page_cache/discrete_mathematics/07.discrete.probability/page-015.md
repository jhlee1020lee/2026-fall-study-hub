---
course: "discrete_mathematics"
source_pdf: "07.Discrete.Probability.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/07.Discrete.Probability.pdf"
generated_at: "2026-10-13T03:36:41Z"
---
 Independence
• Definition: The events E and F are independent if and only if 𝑝 𝐸 ∩ 𝐹 = 𝑝 𝐸 𝑝 𝐹
  – Intuitively, 𝐸 is independent of 𝐹 if 𝑝 𝐸 𝐹 = 𝑝 𝐸
                                    𝑝 𝐸∩𝐹
  – It follows that 𝑝 𝐸 = 𝑝 𝐸 𝐹   =         and thus 𝑝 𝐸 ∩ 𝐹 = 𝑝 𝐸 𝑝 𝐹
                                     𝑝 𝐹



• Example: Suppose E is the event that a randomly generated bit string of length four begins
  with a 1 and F is the event that this bit string contains an even number of 1s. Are E and F
  independent if the 16 bit strings of length four are equally likely?
• Solution: There are eight bit strings of length four that begin with a 1, and eight bit strings
  of length four that contain an even number of 1s.
                                                              1
  – Since the number of bit strings of length 4 is 16, 𝑝 𝐸 =
                                                              2
                                                            1
  – Since 𝐸 ∩ 𝐹 = {1111, 1100, 1010, 1001}, 𝑝 𝐸 ∩ 𝐹 = , we conclude that 𝐸 and 𝐹 are
                                                            4
    independent because 𝑝 𝐸 ∩ 𝐹 = 𝑝 𝐸 ⋅ 𝑝 𝐹
