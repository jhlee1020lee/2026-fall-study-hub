---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
equals() Example
 class Shoes {
   String company, model;
   int size;

     Shoes(String company, String model, int size) {
       this.company = company; this.model = model; this.size = size;
     }

     @Override
     public boolean equals(Object o) {
        ...
     }
 }

                                    Jaemin Yoo (SNU)                   19
