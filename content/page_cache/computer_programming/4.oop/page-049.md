---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 49
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Swap: Primitive Types
class Test {
   static void swap(int a, int b) {
       int temp;
       temp = a;
       a = b;
       a = temp;
   }

    public static void main(String[] args) {
        int x = 2, y = 3;
        swap(x, y);
        System.out.println(x + " " + y);
    }
}

                                         Jaemin Yoo (SNU)   49
