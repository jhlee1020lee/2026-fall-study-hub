---
course: "computer_architecture"
source_pdf: "lec.04.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf"
generated_at: "2026-09-14T23:38:17Z"
---
                        It is all about time
  Performance = 1 / Time

    ➟ Shorter latency ⇒ higher performance
    ➟ Higher throughput (job/time) ⇒ higher performance

  UNIX “time” command
    ➟ Elapsed time                          // wall-clock time
    ➟ User CPU time                         // time spent running your code
    ➟ System CPU time                       // time spent running other code
                                               on behalf of your code

  Elapsed time – ( user CPU time + system CPU time)
  // time running other code unrelated to your code (other processes, I/O, …)


1. Be precise about what you measured when reporting
2. Measure & report wall-clock time on unloaded system


                                                                                4 / 23
