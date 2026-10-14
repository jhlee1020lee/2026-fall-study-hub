---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 27
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
10 mins

Problem2 - Producer and Consumer
● Implement public void run() method of Producer and
  Consumer class.
● The run method of the Producer class adds a Work object to
  the workQueue.
   ○ Assume that the capacity of workQueue is 20. If the workQueue is full,
     the producer cannot add a work to the workQueue.
● The run method of the Consumer class probabilistically (50%)
  takes out a Work object to the workQueue.
