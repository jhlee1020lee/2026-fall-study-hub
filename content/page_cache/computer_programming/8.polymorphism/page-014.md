---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Why Overloading?
• Case 3: Supply additional information to the method.

  String dna = new String("TACGAAGTTACTCGCTGTCAGATCGTAAGCGACGCGATCGTAATGTGAAT");

  // Find first occurrence of “CGC”
  int first = dna.indexOf("CGC");

  // Find occurance of “CGC” after the first occurence of “CGC”
  int second = dna.indexOf("CGC", first + "CGC".length());

  System.out.println(first + ", " + second); // 12, 32


                                      Jaemin Yoo (SNU)                             14
