---
course: "computer_architecture"
source_pdf: "lec.09.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.09.pdf"
generated_at: "2026-10-13T03:36:13Z"
---
                  Security implication?
 The PC+4 prediction allows a processor to access data in advance

   ➟ But what if the data is confidential?

1 if (you_have_privilege) {
2     accesss_privileged_data();
3 }

 It seems fine in the architectural viewpoint, but in microarchitectural
 viewpoint…

   ➟ The processor actually accesses the privileged data
   ➟ It changes microarchitectural states (eg, cache!)
   ➟ It leaks the confidential data!

 Microarchitectural vulnerability

   ➟ Ex) Spectre, Meltdown, …
   ➟ We will discuss about it after we learn more about cache
                                                                           33 / 33
