---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overloading Principles
• Only one of the overloading methods should do most of the work.

class MyClass {
   public int var1 = 0;
   void debug() { System.out.println("var 1 : " + this.var1); }

    // version 1
    void debug(String s) { System.out.println(s + "var 1 : " + this.var1); }

    // version 2; which is better?
    void debug(String s) { System.out.print("Output : " + s); debug(); }
}


                                    Jaemin Yoo (SNU)                           16
