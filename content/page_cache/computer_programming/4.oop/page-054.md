---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 54
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Swap: Wrapper Class

class Test {
   class Wrapper {
      String s;
          Wrapper(String s) { this.s = s; }
   }

    static void swap(Wrapper a, Wrapper b) {
        String temp;
        temp = a.s;
        a.s = b.s;
        a.s = temp;
    }
}


                                         Jaemin Yoo (SNU)   54
