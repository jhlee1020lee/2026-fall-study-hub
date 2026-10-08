---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 32
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
        Impact of Stall on Performance

Without stall

  ➟ Ideal IPC = 1
With stall

  ➟ Each stall cycle corresponds to 1 lost cycle
  ➟ For a program with N instructions and S stall cycles,
   Average IPC (with stall) = N / (N+S)
S depends on

  ➟ Frequency of hazard-causing dependencies
  ➟ Distance between hazard-causing instruction pairs
  ➟ Distance between hazard-causing dependencies




                                                            32 / 51
