---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 58
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Generic Constructors
• Constructors declaring one or more type variables.
  • A constructor can be generic, whether the class is itself generic or not.

  class Test {
     public <T> Test(T item) {
         print(item.toString());
         print(item.getClass().getName());
     }
     void print(String s) { System.out.print(s + "|"); }
  }

  Test test1 = new Test("Generic");               // Generic|java.lang.String|
  System.out.println();
  Test test2 = new Test(111);                     // 111|java.lang.Integer|

                                      Jaemin Yoo (SNU)                           58
