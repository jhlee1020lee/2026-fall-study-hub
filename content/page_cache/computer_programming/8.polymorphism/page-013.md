---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Why Overloading?
• Case 2: Handle slightly different, but closely related tasks.

  static double abs_add(double a, double b) { return Math.abs(a) + Math.abs(b); }
  static double abs_add(double[] arr) {
     double sum = 0;
     for(int index = 0; index < arr.length; ++index) {
         sum = abs_add(sum, arr[index]);
     }
     return sum;
  }


  double[] arr = new double[]{1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0};
  System.out.println(abs_add(arr));

                                      Jaemin Yoo (SNU)                              13
