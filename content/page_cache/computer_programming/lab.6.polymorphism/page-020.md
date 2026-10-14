---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 20
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
Main Class: Managing WorkQueue
● Initialize with Works
● Workers will insert and pop works.
● Queue API
   ○ Insert          : workQueue.add(new Work());
   ○ Take out: Work work = workQueue.poll();



Queue<Work> workQueue;
workQueue = new LinkedList<>();
for(int i = 0; i < numWorks; i++){
    workQueue.add(new Work());
}
