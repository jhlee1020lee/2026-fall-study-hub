---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 28
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Multiple Inheritance

   class D {
      public int var = 0;
      public void f() { var = 1; }
   }

   class A extends D { public void f() { var = 2; } }
   class B extends D { public void f() { var = 3; } }
   class C extends A, B { public void g() { f(); } }

   // Java cannot determine either f() from A or f() from B

                            Jaemin Yoo (SNU)                  28
