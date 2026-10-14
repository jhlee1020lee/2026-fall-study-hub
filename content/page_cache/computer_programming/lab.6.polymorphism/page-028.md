---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 28
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
10 mins

Problem2 - Producer and Consumer
● Add report message to the public void run() method of
  Producer and Consumer class.
   ○ Implement the report() method in Worker class and use it in the run()
     method of Producer and Consumer class.
   ○ When the producer produces a work, print (except {, })
     “worker{Worker ID} produced work{Work ID}”
   ○ When the producer fails to produce a work (workQueue is full), print
     “worker{Worker ID} failed to produce work”
   ○ When the consumer consumes a work, print
     “worker{Worker ID} consumed work{Work ID}”
   ○ When the consumer fails to consume a work (1/2 probability failure or
     no work in the workQueue), print
     “worker{Worker ID} failed to consume work”
