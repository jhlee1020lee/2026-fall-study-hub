---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 39
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Type Casting for Instance Methods
• Overridden methods cannot be called with type casting.
  class T1 {
      String s() { return "1"; }
  }
  class T2 extends T1 {
      String s() { return "2"; }
  }
  class T3 extends T2 {
      String s() { return "3"; }
      void test() {
          System.out.println("s()            = " + s());              // 3
          System.out.println("((T2)this).s() = " + ((T2)this).s());   // 3
          System.out.println("((T1)this).s() = " + ((T1)this).s());   // 3
      }
  }

                                           Jaemin Yoo (SNU)                  39
