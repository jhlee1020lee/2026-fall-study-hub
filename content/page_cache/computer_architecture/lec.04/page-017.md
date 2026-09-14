---
course: "computer_architecture"
source_pdf: "lec.04.pdf"
pdf_page: 17
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf"
generated_at: "2026-09-14T23:38:17Z"
---
                     Harmonic Mean

Don’t take arithmetic mean of “rates” (e.g. throughput, IPC)
  ➟ e.g. 30 km/h for first 10 km, 90 km/h for next 10 km,
   the average speed is not (30 + 90)/2 = 60 km/h!

To compute average rate
  1. Expand fully
     average speed = total distance / total time
     = 20 / (10/30 + 10/90) = 45 km/h
  2. Harmonic mean & weighed harmonic mean

                     n                               1
      HM =      n−1 1                   WHM =    n    wi
                                                ∑i=1 Rate
                                    ​                                 ​




               ∑i=0 Ratei
                                                         ​




                                                     ​            ​




                                                          i
                      ​         ​




                                                              ​



                            ​




                                                                          17 / 23
