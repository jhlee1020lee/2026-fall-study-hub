---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 37
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Method Call: Call-by-Value
• The following code is intended to swap two variables’ values.
class Test {
   static void swap(int a, int b) {
       int temp;
       temp = a;
       a = b;
       b = temp;
   }
   public static void main(String[] args) {
       int a = 2, b = 3;
       swap(a, b);
       System.out.println(a + " " + b);
   }
}

                                        Jaemin Yoo (SNU)          37
