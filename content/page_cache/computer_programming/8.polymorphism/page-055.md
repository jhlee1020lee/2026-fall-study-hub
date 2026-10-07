---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 55
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Generic Class: Static Members
• Referring T on static member declaration incurs an error.


  class Wrapper<T> {
     T obj;
     void add(T obj) { this.obj = obj; }
     T get() { return obj; }

      static T shared;                           // error
      static void set(T value) { }               // error
  }



                                     Jaemin Yoo (SNU)         55
