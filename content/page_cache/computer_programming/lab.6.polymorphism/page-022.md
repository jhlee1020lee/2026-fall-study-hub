---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
Main Class: Managing Workers
● The scheduler schedules a worker.
● Selected worker (producer / consumer) runs.

Scheduler<Worker> scheduler = new Scheduler<>(workers);
while(!(workQueue.isEmpty())){
    System.out.printf("Scheduling work... (Remaining
work: %d)\n", workQueue.size());
    Worker worker = scheduler.schedule();
    if (worker != null) {
        worker.run();
    }
    Scheduler.delay();
}
