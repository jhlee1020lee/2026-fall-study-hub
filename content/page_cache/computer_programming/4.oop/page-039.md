---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 39
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Method Call: Call-by-Value
                                                             Memory
• Memory state right before the function returns.
                                                           main function
class Test {
   static void swap(int a, int b) {                         a       2
       int temp;
       temp = a;                                            b       3
       a = b;
       b = temp;                                           swap function
   }
   public static void main(String[] args) {                 a       3
       int a = 2, b = 3;
       swap(a, b);                                          b       2
       System.out.println(a + " " + b);
                                                           temp     2
   }
}

                                        Jaemin Yoo (SNU)                   39
