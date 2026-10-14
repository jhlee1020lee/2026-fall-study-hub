---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 34
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
10 mins

Problem3.2 - Fair Scheduler

● Implement T scheduleFair() method in Scheduler class.
   ○ Return the worker who wasn’t scheduled for the longest time.
   ○ To implement this scheduling policy, define additional member variable
     in Worker class that tracks how long the worker wasn’t scheduled.
   ○ (Hint) Change the Scheduler<T> to Scheduler<T extends
      Worker> so that you can access the members of Worker.
