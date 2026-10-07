---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 53
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Generic Class
• A class declaring one or more type variables.
   • Syntax: class C<T1,...,Tn>.

  class Wrapper<T> {
     T obj;
     void add(T obj) { this.obj = obj; }
     T get() { return obj; }
  }

  Wrapper<Integer> m = new Wrapper<Integer>();
  m.add(2);
  System.out.println(m.get());

                                   Jaemin Yoo (SNU)   53
