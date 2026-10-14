---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
Worker class
public abstract class Worker {
    ...
    public abstract void run();
    void report(String msg){
        // TODO: problem2
    }
}
class Producer extends Worker {
    Producer(Queue<Work> workQueue) { super(workQueue); }
    public void run() {
        // TODO: problem2
    }
}
class Consumer extends Worker {
    Consumer(Queue<Work> workQueue) { super(workQueue); }
    public void run() {
        // TODO: problem2
    }
}
