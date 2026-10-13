---
course: "computer_programming"
source_pdf: "9.collections.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.pdf"
generated_at: "2026-10-13T15:42:46Z"
---
Set Operation Example 1

 import java.util.HashSet;
 import java.util.Set;

 public class SetTest {
     public static void main(String[] args) {
         Set<Integer> set = new HashSet<>();
         for (int i = 0; i < 10; i++) { set.add(i % 7); }
         System.out.println(set);
         System.out.println(set.contains(5) + " " + set.contains(7));
     }
 }

 [0, 1, 2, 3, 4, 5, 6]
 true false


                                     Jaemin Yoo (SNU)                   43
