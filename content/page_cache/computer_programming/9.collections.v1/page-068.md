---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 68
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
PriorityQueue Example
 import java.util.PriorityQueue;
 import java.util.Queue;

 public class QueueTest {
     public static void main(String[] args) {
         Queue<Integer> queue = new PriorityQueue<>();
         int[] arr = {2, 1, 3, 6, 2, 4, 7, 0};
         for (int e : arr) { queue.add(e); }
         System.out.println(queue);                   // [0, 1, 3, 2, 2, 4, 7, 6]
         while (!queue.isEmpty()) {
             System.out.print(queue.poll() + " ");
         }
         System.out.println();                        // 0 1 2 2 3 4 6 7
     }
 }

                                      Jaemin Yoo (SNU)                              68
