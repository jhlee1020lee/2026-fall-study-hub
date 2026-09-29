---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 40
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Comparable<T> Example: Strings
• Compares two String values lexicographically
• Let’s see how the String class is actually implemented.



  public final class String implements ... Comparable<String> {
     private final char[] value;

      ...
  }


                             Jaemin Yoo (SNU)                     40
