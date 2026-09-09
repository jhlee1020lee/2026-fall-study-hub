---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 51
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Swap: Non-Primitive Types
class Test {
   static void swap(String a, String b) {
       String temp;
       temp = a;
       a = b;
       a = temp;
   }

    public static void main(String[] args) {
        String s1 = ”Hi”, s2 = ”all”;
        swap(s1, s2);
        System.out.println(s1 + " " + s2);
    }
}

                                         Jaemin Yoo (SNU)   51
