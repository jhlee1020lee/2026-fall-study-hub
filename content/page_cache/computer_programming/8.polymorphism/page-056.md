---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 56
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Generic Methods
• A method declaring one or more type variables.
  • Type arguments may either be inferred or passed explicitly.


  class ArrayPrinter {
     public static <E> void printArray(E[] elements) {
       for(E element : elements) {
           System.out.print(element.toString() + " ");
       }
    }
  }

                                  Jaemin Yoo (SNU)                56
