---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
private Methods


 boolean sell(int num) {
                                               private boolean inStock(int num) {
    if (inStock(num)) {
                                                  int shortage = num - stock;
       balance += 2000 * num;
                                                  if (shortage > 0) {
       stock -= num;
                                                     return false;
       return true;
                                                  } else {
    } else {
                                                     return true;
       return false;
                                                  }
    }
                                               }
 }



                                Jaemin Yoo (SNU)                                    14
