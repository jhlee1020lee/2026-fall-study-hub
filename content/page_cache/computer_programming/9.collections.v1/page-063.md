---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 63
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
Queue Interface Example

 // LinkedList is a normal queue implementation
 import java.util.LinkedList;
 import java.util.Queue;

 public class QueueTest {
     public static void main(String[] args) {
         Queue<Integer> queue = new LinkedList<>();
         int[] arr = {2, 1, 3, 6, 2};
         for (int e : arr) { queue.add(e); }
         System.out.println(queue);                     // [2, 1, 3, 6, 2]
         System.out.println(queue.poll());              // 2
         System.out.println(queue);                     // [1, 3, 6, 2]
     }
 }


                                     Jaemin Yoo (SNU)                        63
