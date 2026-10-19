---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 56
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
Comparator Example: Comparators

 class NameComp implements Comparator<Player> {
     public int compare(Player e1, Player e2) {
         return e1.getName().compareTo(e2.getName());
     }
 }

 class IdComp implements Comparator<Player>{
     public int compare(Player e1, Player e2) {
         return e1.getId().compareTo(e2.getId());
     }
 }

                               Jaemin Yoo (SNU)         56
