---
course: "computer_architecture"
source_pdf: "lec.02.pdf"
pdf_page: 27
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf"
generated_at: "2026-09-09T01:11:46Z"
---
                      General Purpose
General Purpose = effective support for “large and small, separate and mixed
applications” in many domains (e.g., commercial, scientific, real-time…)


How
  ➟ Code-independent operation
       ➟ No special interpretation of bit pattern in data
            ➟ e.g. ASCII character has no special significance.
       ➟ Except where essential
            ➟ e.g., Integer, floating point, etc
  ➟ Support full generality of logic manipulation on bit and data entities
  ➟ Fine-grain memory addressability (Byte unit? Bit unit?)


But.. what about ML accelerators?
  ➟ Sacrifce the generality for the performance.

                                                                               27 / 29
