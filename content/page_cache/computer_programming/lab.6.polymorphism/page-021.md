---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 21
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
Main Class: Managing Workers
● Working Group for managing the workers, each worker of type
  Producer or Consumer.
  ○ List<Worker> : List of Workers
● Working Group contains derived classes of the Worker.

List<Worker> workers;
workers = new LinkedList<>();
for (int i = 0; i < numProducers; i++) {
    workers.add(new Producer(workQueue));
}
for (int i = 0; i < numConsumers; i++) {
    workers.add(new Consumer(workQueue));
}
