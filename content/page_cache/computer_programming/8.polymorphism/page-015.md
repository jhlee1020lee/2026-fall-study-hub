---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Why Overloading?
• Case 4: Supply default values for the parameters.

  static double power(double input, int n) {
     if(n <= 0) return 1;
     return input * power(input, n-1);
  }
  static double power(double input) {
     return power(input, 2);
  }


  System.out.println(power(2, 10));
  System.out.println(power(2));

                                      Jaemin Yoo (SNU)   15
