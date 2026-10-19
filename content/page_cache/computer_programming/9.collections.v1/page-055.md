---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 55
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
Comparator Example: Class
 class Player {
     String name; int id;
     public String getName() { return name; }
     public Integer getId() { return id; }

     public Player(String name, int id) {
         this.name = name; this.id = id;
     }

     @Override
     public String toString() {
         return name + '(' + id + ')';
     }
 }

                                     Jaemin Yoo (SNU)   55
