---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 51
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
TreeSet Example
 import java.util.*;
 public class SetTest {
     public static void main(String[] args) {
         Set set = new TreeSet();
         List list = new LinkedList<>(Arrays.asList(2, 1, 3, 6, 2, 4, 7, 0));
         System.out.println(list);
         set.addAll(list);
         System.out.println(set);
     }
  }

 [2, 1, 3, 6, 2, 4, 7, 0]
 [0, 1, 2, 3, 4, 6, 7]

                                  Jaemin Yoo (SNU)                              51
