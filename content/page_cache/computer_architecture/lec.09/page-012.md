---
course: "computer_architecture"
source_pdf: "lec.09.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.09.pdf"
generated_at: "2026-10-13T03:36:13Z"
---
Alternative: Branch Prediction → Predict not-taken or PC+4

    Instead of stalling, guess nextPC = PC+4 to keep fetching every cycle

      ➟ Is this a good guess?
      ➟ For how many instructions is the next PC PC+4?

    ~20% of the instruction mix is control flow

      ➟ ~50% of “forward” control flow (i.e., if-then-else) is taken
      ➟ ~90% of “backward” control flow (i.e., loop back) is taken
          ➟ Overall, typically ~70% taken and ~30% not taken
           [Lee and Smith, 1984]

    Expect “nextPC = PC+4” ~86% of the time, but what about the
    remaining 14%?

      ➟ What do you lose if you guessed incorrectly?

                                                                            12 / 33
